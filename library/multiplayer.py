import pyxel
import socket
import select
import json
import struct
import time


MAX_WAIT_FOR_DATA_SEC = 0.5


class DisconnectError(Exception):
  pass


class Multiplayer:
  def __init__(self, port):
    self.port = port
    self.server = MultiplayerServer(port=port)
    self.client = MultiplayerClient()
    self._is_primary = True

  @property
  def is_on_lan(self):
    return self.my_ip != '0.0.0.0'

  @property
  def my_ip(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()
    return my_ip

  @property
  def is_connected(self):
    return self.server.is_connected

  @property
  def is_primary(self):
    return self._is_primary

  def connect(self, host, port):
    self.client.connect(host, port)
    self._is_primary = False

  def send(self, message):
    try:
      if self.is_primary:
        self.server.send(message)
      else:
        self.client.send(message)
    except BrokenPipeError:
      raise DisconnectError()

  def check_for_received_message(self):
    if self.is_primary:
      return self.server.check_for_received_message()
    else:
      return self.client.check_for_received_message()

  def start_new_game(self):
    if self.is_primary:
      self.server.game_id = time.time()

class MultiplayerServer:
  def __init__(self, port):
    self.port = port
    self.sock = None
    self.client = None
    self.client_addr = None
    self.game_id = None

  @property
  def is_started(self):
    return self.sock is not None

  @property
  def is_connected(self):
    return self.client is not None

  def start(self):
    self.sock = socket.socket()
    self.sock.bind(('127.0.0.1', self.port))
    self.sock.listen(1)

  def check_for_connection(self):
    # poll the socket (timeout=0 ==> non-blocking poll)
    read, _, _ = select.select([self.sock], [], [], 0.0)
    if read:
      self.client, self.client_addr = self.sock.accept()
      return True
    return False

  def send(self, message):
    if not self.is_connected:
      raise RuntimeError("Not connected!")

    _send(self.client, message, self.game_id)

  def check_for_received_message(self):
    while True:
      message = _check_for_received_message(self.client)
      if message.pop('game_id', None) == self.game_id:
        return message

  def shutdown(self):
    if self.client:
      self.client.shutdown()
      self.client.close()
      self.client = None
      self.client_addr = None

    if self.sock:
      self.sock.shutdown()
      self.sock.close()
      self.sock = None


class MultiplayerClient:
  def __init__(self):
    self.host = None
    self.port = None
    self.server = None
    self.game_id = None

  def connect(self, host, port):
    self.host = host
    self.port = port
    self.server = socket.socket()
    print(f"About to connect! Host: {host}, Port: {port}")
    self.server.connect((self.host, self.port))
    print("Connected!")

  def send(self, message):
    if not self.server:
      raise RuntimeError("Not connected!")

    _send(self.server, message, self.game_id)

  def check_for_received_message(self):
    message = _check_for_received_message(self.server)
    self.game_id = message.pop('game_id', None)
    return message


_HEADER_FORMAT_STR = '!I'
_HEADER_LEN = 4


def _send(sock, data, game_id):
  """
  |  |  |  |  |  |  | ... |  |
  |<- 4B Len->|<--  data  -->|
  """

  data['game_id'] = game_id
  print("message being sent", data)
  # Convert the data to a json str as bytes
  data_as_json_bytes = str.encode(json.dumps(data))

  # We'll write an unsigned int header in big-endian for how long the payload will be
  packed_len = struct.pack(_HEADER_FORMAT_STR, len(data_as_json_bytes))
  assert(len(packed_len) == _HEADER_LEN)

  # ship it!
  sock.send(packed_len)
  sock.send(data_as_json_bytes)


def _check_for_received_message(sock):
  read, _, _ = select.select([sock], [], [], MAX_WAIT_FOR_DATA_SEC)
  if not read:
    raise DisconnectError()

  try:
    packed_message_len = sock.recv(_HEADER_LEN)
  except ConnectionResetError:
    raise DisconnectError()

  if len(packed_message_len) != _HEADER_LEN:
    raise DisconnectError()

  message_len = struct.unpack(_HEADER_FORMAT_STR, packed_message_len)[0]
  try:
    data = sock.recv(message_len)
  except ConnectionResetError:
    raise DisconnectError()
  message = json.loads(data.decode())
  print("message being received", message)
  return message

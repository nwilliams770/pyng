import pyxel
import socket
import select
import json
import struct

class Multiplayer:
  def __init__(self, port):
    self.port = port
    self.server = MultiplayerServer(port=port)
    self.client = MultiplayerClient()
    self._is_primary = True

    self.server.start()

  @property
  def is_primary(self):
    return self._is_primary

  def connect(self, host, port):
    self.client.connect(host, port)
    self._is_primary = False


class MultiplayerServer:
  def __init__(self, port):
    self.port = port
    self.sock = None
    self.client = None
    self.client_addr = None

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

    _send(self.client, message)

  def check_for_received_message(self):
    return _check_for_received_message(self.client)

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

  def connect(self, host, port):
    self.host = host
    self.port = port
    self.server = socket.socket()
    self.server.connect((self.host, self.port))

  def send(self, message):
    if not self.server:
      raise RuntimeError("Not connected!")

    _send(self.server, message)

  def check_for_received_message(self):
    return _check_for_received_message(self.server)


_HEADER_FORMAT_STR = '!I'
_HEADER_LEN = 4


def _send(sock, data):
  """
  |  |  |  |  |  |  | ... |  |
  |<- 4B Len->|<--  data  -->|
  """

  # Convert the data to a json str as bytes
  data_as_json_bytes = str.encode(json.dumps(data))

  # We'll write an unsigned int header in big-endian for how long the payload will be
  packed_len = struct.pack(_HEADER_FORMAT_STR, len(data_as_json_bytes))
  assert(len(packed_len) == _HEADER_LEN)

  # ship it!
  sock.send(packed_len)
  sock.send(data_as_json_bytes)


def _check_for_received_message(sock):
  read, _, _ = select.select([sock], [], [], 0.0)
  if read:
    packed_message_len = sock.recv(_HEADER_LEN)
    message_len = struct.unpack(_HEADER_FORMAT_STR, packed_message_len)[0]
    data = sock.recv(message_len)
    message = json.loads(data.decode())
    return message
  return None

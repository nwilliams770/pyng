import pyxel
import ipaddress

import constants
from .menu_state import LanConnectMenuState
from label import key_cap_label, ray_label
from library import multiplayer


class LANConnectMenu():
  def __init__(self, multiplayer):
    self.state = LanConnectMenuState.COLLECTING_INPUT
    self.frame = 0
    self.multiplayer = multiplayer
    self.navigate_to_menu = False
    self.connected = False

    self.waiting_for_connection_label = ray_label.RayLabel("You:", size=4.0, colors=(12, 13), origin=(constants.GAME_WIDTH * .5, 40), alignment=ray_label.Alignment.CENTER)
    self.my_ip_label = ray_label.RayLabel(self.multiplayer.my_ip, size=6.0, colors=(6, 7), origin=(constants.GAME_WIDTH * .5, 58), alignment=ray_label.Alignment.CENTER)
    self.connecting_label = ray_label.RayLabel("Connecting...", size=4.0, colors=(1, 1), origin=(constants.GAME_WIDTH * .5, 79), alignment=ray_label.Alignment.CENTER)
    self.opponent_found_label = ray_label.RayLabel("Opponent Found", size=4.0, colors=(4, 5), origin=(constants.GAME_WIDTH * .5, 79), alignment=ray_label.Alignment.CENTER)

    self.input_label = ray_label.RayLabel("Opponent:", size=4.0, colors=(12, 13), origin=(constants.GAME_WIDTH * .5, 100), alignment=ray_label.Alignment.CENTER)
    self.ip_input = IpInput(center=(constants.GAME_WIDTH * .5, self.input_label.bottom + 16))

    self.error_label = ray_label.RayLabel("Connection Error Please Try Again", size=4.0, colors=(8, 9), origin=(constants.GAME_WIDTH * .5, self.input_label.bottom + self.ip_input.input_box_height + 14), alignment=ray_label.Alignment.CENTER)

    self.submit_label = ray_label.RayLabel("Submit", size=4.0, colors=(12, 13), origin=(constants.GAME_WIDTH * .5 + 27, 162), alignment=ray_label.Alignment.CENTER)
    self.submit_key_cap = key_cap_label.KeyCapLabel(key_str="Enter", key_code=pyxel.KEY_ENTER, size=4.0, origin=(constants.GAME_WIDTH * .5 - 12, self.submit_label.top + 2), alignment=ray_label.Alignment.CENTER)
    self.footer_label = ray_label.RayLabel("Return to Main Menu", size=4.0, colors=(12, 13), origin=(constants.GAME_WIDTH * .5 + 13, 178), alignment=ray_label.Alignment.CENTER)
    self.footer_key_cap = key_cap_label.KeyCapLabel(key_str="M", key_code=pyxel.KEY_M, size=4.0, origin=(constants.GAME_WIDTH * .5 - 47, self.footer_label.top + 2), alignment=ray_label.Alignment.CENTER)

  def update(self):
    if self.state == LanConnectMenuState.COLLECTING_INPUT:
      # Whenever we're on the multiplayer screen, make sure we're running our server
      # so someone can connect to us.
      # Also, each frame, check if someone has connected.
      if not self.multiplayer.server.is_started:
        self.multiplayer.server.start()

      if self.multiplayer.server.check_for_connection():
        self.state = LanConnectMenuState.OPPONENT_FOUND

      # User navigated back to main menu
      if pyxel.btn(self.footer_key_cap.key_code):
        self.ip_input.clear()
        self.navigate_to_menu = True

      self.ip_input.update()

      if pyxel.btnp(pyxel.KEY_ENTER) and not self.ip_input.input_empty:
        # clear any prev errors
        self.clear_connection_error()
        self.state = LanConnectMenuState.CONNECTING

    elif self.state == LanConnectMenuState.CONNECTING:
      self.frame += 1

      if self.frame == 90:
        host = self.ip_input.value
        try:
          self.multiplayer.connect(host=host, port=5000)
          self.state = LanConnectMenuState.OPPONENT_FOUND
        except ConnectionError as e:
          print(e)
          self.connection_error()
          self.state = LanConnectMenuState.COLLECTING_INPUT

        self.frame = 0

    elif self.state == LanConnectMenuState.OPPONENT_FOUND:
      self.frame += 1

      if self.frame == 60:
        self.connected = True
        self.frame = 0
        self.reset()

  def draw(self):
    self.my_ip_label.draw()
    self.waiting_for_connection_label.draw()
    self.ip_input.draw()
    self.input_label.draw()
    self.submit_label.draw()
    self.submit_key_cap.draw()
    self.footer_label.draw()
    self.footer_key_cap.draw()

    if self.ip_input.connection_error:
      self.error_label.draw()

    if self.state == LanConnectMenuState.CONNECTING and pyxel.frame_count % 30 > 15:
      self.connecting_label.draw()

    if self.state == LanConnectMenuState.OPPONENT_FOUND:
      self.opponent_found_label.draw()


  def connection_error(self):
    self.ip_input.connection_error = True

  def clear_connection_error(self):
    self.ip_input.connection_error = False

  def reset(self):
    self.ip_input.clear()
    self.state = LanConnectMenuState.COLLECTING_INPUT

class IpInput:
  def __init__(self, center):
    longest_input = "255.255.255.255"
    self.max_chars = len(longest_input)

    text_size = 6.0

    # generate a throw-away label to see how big a max-length label could be
    label_for_size = ray_label.RayLabel(longest_input + "1", size=text_size)

    # Pad around the labels
    label_origin = (center[0] - label_for_size.width / 2, center[1])
    self.origin = (label_origin[0] - 4, label_origin[1] - label_for_size.height/2 - 4)
    self.input_box_width = label_for_size.width + 8
    self.input_box_height = label_for_size.height + 9

    self.input_placeholder_label = ray_label.RayLabel("IPv4 Address", size=text_size, colors=(12, 13), origin=label_origin, alignment=ray_label.Alignment.LEFT)
    self.input_label = ray_label.RayLabel("", size=text_size, colors=(1, 1), origin=label_origin, alignment=ray_label.Alignment.LEFT)

    self.value = ''
    self.connection_error = False

    self.valid_inputs = {
      pyxel.KEY_0: '0',
      pyxel.KEY_1: '1',
      pyxel.KEY_2: '2',
      pyxel.KEY_3: '3',
      pyxel.KEY_4: '4',
      pyxel.KEY_5: '5',
      pyxel.KEY_6: '6',
      pyxel.KEY_7: '7',
      pyxel.KEY_8: '8',
      pyxel.KEY_9: '9',
      pyxel.KEY_PERIOD: '.'
    }

  @property
  def input_empty(self):
    return len(self.value) == 0

  def _is_under_char_limit(self):
    return len(self.value) <= self.max_chars

  def clear(self):
    self.value = ''
    self.input_label.set_text(self.value)

  def update(self):
    for key in self.valid_inputs.keys():
      if pyxel.btnp(key) and self._is_under_char_limit():
        self.value += self.valid_inputs[key]
        self.input_label.set_text(self.value)

    if pyxel.btnp(pyxel.KEY_BACKSPACE) and self.value:
      self.connection_error = False
      self.value = self.value[0:len(self.value) - 1]
      self.input_label.set_text(self.value)

  def draw(self):
    if self.input_empty:
      self.input_placeholder_label.draw()
    else:
      self.input_label.draw()

    pyxel.rectb(self.origin[0], self.origin[1], self.input_box_width, self.input_box_height, 8 if self.connection_error else 12)

    # draw a blinking cursor
    if pyxel.frame_count % 30 > 15:
      cursor_x = self.input_label.origin[0] + self.input_label.width + 1
      pyxel.line(cursor_x, self.input_placeholder_label.top - 1, cursor_x, self.input_placeholder_label.bottom + 1, col=2)

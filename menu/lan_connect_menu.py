import pyxel
import ipaddress

import constants
from label import ray_label
from library import multiplayer

"""
# TODO:
# - get IP input looking good,
# - fix validation (onnly show green for good IP)
  - show user's ip address
  - show waiting to connect
  - sohw notification when connected

"""


class LANConnectMenu():
  def __init__(self, multiplayer):
    self.multiplayer = multiplayer
    self.navigate_to_menu = None
    self.valid_input_submitted = None

    self.waiting_for_connection_label = ray_label.RayLabel("You:", size=4.0, colors=(12, 13), origin=(constants.GAME_WIDTH / 2, 40), alignment=ray_label.Alignment.CENTER)
    self.my_ip_label = ray_label.RayLabel(self.multiplayer.my_ip, size=6.0, colors=(6, 7), origin=(constants.GAME_WIDTH / 2, 58), alignment=ray_label.Alignment.CENTER)

    self.input_label = ray_label.RayLabel("Opponent:", size=4.0, colors=(12, 13), origin=(constants.GAME_WIDTH / 2, 100), alignment=ray_label.Alignment.CENTER)
    self.ip_input = IpInput(center=(constants.GAME_WIDTH / 2, self.input_label.bottom + 16))

  def update(self):
    self.ip_input.update()

  def draw(self):
    self.my_ip_label.draw()
    self.waiting_for_connection_label.draw()
    self.ip_input.draw()
    self.input_label.draw()


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
    self.width = label_for_size.width + 8
    self.height = label_for_size.height + 8

    self.input_placeholder_label = ray_label.RayLabel("IPv4 Address", size=text_size, colors=(12, 13), origin=label_origin, alignment=ray_label.Alignment.LEFT)
    self.input_label = ray_label.RayLabel("", size=text_size, colors=(1, 1), origin=label_origin, alignment=ray_label.Alignment.LEFT)

    self.value = ''
    self.input_error = False
    self.input_submitted = False

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

  def _is_valid_input(self):
    try:
      ipaddress.IPv4Address(self.value)
      return True
    except ValueError:
      return False

  def _validate_input(self):
    if self._is_valid_input() and not self.input_empty:
      self.input_error = False
    else:
      self.input_error = True

  def update(self):
    for key in self.valid_inputs.keys():
      if pyxel.btnp(key) and self._is_under_char_limit():
        self.value += self.valid_inputs[key]
        self.input_label.set_text(self.value)
        self._validate_input()

    if pyxel.btnp(pyxel.KEY_BACKSPACE) and self.value:
      self.value = self.value[0:len(self.value) - 1]
      self.input_label.set_text(self.value)
      self._validate_input()

    if pyxel.btnp(pyxel.KEY_ENTER):
      print("Submit attempted:\t{}".format(self.value))
      if not self.input_error:
        self.input_submitted = True

  def draw(self):
    if self.input_empty:
      self.input_placeholder_label.draw()
    else:
      self.input_label.draw()

    pyxel.rectb(self.origin[0], self.origin[1], self.width, self.height, 8 if self.input_error and self.value else 12)

    # draw a blinking cursor
    if pyxel.frame_count % 30 > 15:
      cursor_x = self.input_label.origin[0] + self.input_label.width + 1
      pyxel.line(cursor_x, self.input_label.top - 2, cursor_x, self.input_label.bottom + 2, col=2)

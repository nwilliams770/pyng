import pyxel
import ipaddress

import constants
from label import ray_label



class LANConnectMenu():
  def __init__(self):
    self.navigate_to_menu = None
    self.valid_input_submitted = None
    self.waiting_for_connection_label = ray_label.RayLabel("Waiting for a player to connect...", size=16, colors=(1, 1), origin=(constants.GAME_WIDTH * .25, constants.GAME_HEIGHT * .25), alignment=ray_label.Alignment.CENTER)
    self.ip_input = IpInput()

  def update(self):
    self.ip_input.update()

  def draw(self):
    self.waiting_for_connection_label.draw()
    self.ip_input.draw()


class IpInput:
  def __init__(self):
    self.input_label = ray_label.RayLabel("Connect with a player", size=16, colors=(1, 1), origin=(constants.GAME_WIDTH * .45, constants.GAME_HEIGHT * .45), alignment=ray_label.Alignment.CENTER)
    self.input_width = constants.GAME_WIDTH * .5
    self.input_height = 10
    self.input_placeholder = ray_label.RayLabel("IPv4 Address", size=10, colors=(1,1), origin=(constants.GAME_WIDTH * .65, constants.GAME_HEIGHT * .65), alignment=ray_label.Alignment.CENTER)
    self.value = ''
    self.max_chars = 15 # 255.255.255.255, only concerned with IPv4
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
  def border_x(self):
    pass

  @property
  def border_y(self):
    pass

  @property
  def input_empty(self):
    return len(self.value) < 1

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
        self._validate_input()

    if pyxel.btnp(pyxel.KEY_BACKSPACE):
      self.value = self.value[0:len(self.value) - 1]
      self._validate_input()


    if pyxel.btnp(pyxel.KEY_ENTER):
      print("Submit attempted:\t{}".format(self.value))
      if not self.input_error:
        self.input_submitted = True

  def draw(self):
    pyxel.rectb(constants.GAME_WIDTH / 2 - self.input_width / 2, constants.GAME_HEIGHT * .7, self.input_width, self.input_height, 1 if not self.input_error else 8)
    pyxel.text(30 + 6, 40 + 2, self.value, 1)

    # if self.input_error:
    #   pyxel.text(30, 40 + self.height + 2, "Invalid IP Address", 8)

    if self.input_empty:
      pyxel.text(30 + 12, 40 + 2, "IPv4 Address",1)


  def reset(self):
    self.value = ''

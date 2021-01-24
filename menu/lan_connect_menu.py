import pyxel
import ipaddress

import constants
from label import ray_label



class LANConnectMenu():
  def __init__(self):
    self.navigate_to_menu = None
    self.valid_input_submitted = None
    self.waiting_for_connection_label = ray_label.RayLabel("Waiting for a player to connect...", size=16, colors=(1, 1), origin=(constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 2), alignment=ray_label.Alignment.CENTER)
    # self.ip_input = IpInput()

  def update(self):
    pass

  def draw(self):
    pass


# class IpInput:
#   def __init__(self):
#     self.width = 70
#     self.height = 8
#     self.value = ''
#     self.max_chars = 15 # 255.255.255.255, only concerned with IPv4
#     self.input_error = False
#     self.input_submitted = False
#     self.valid_inputs = {
#       pyxel.KEY_0: '0',
#       pyxel.KEY_1: '1',
#       pyxel.KEY_2: '2',
#       pyxel.KEY_3: '3',
#       pyxel.KEY_4: '4',
#       pyxel.KEY_5: '5',
#       pyxel.KEY_6: '6',
#       pyxel.KEY_7: '7',
#       pyxel.KEY_8: '8',
#       pyxel.KEY_9: '9',
#       pyxel.KEY_PERIOD: '.'
#     }

#   @property
#   def x(self):
#     return self.screen_width / 2 - self.width / 2

#   @property
#   def y(self):
#     return self.screen_height * 2/3

#   @property
#   def input_empty(self):
#     return len(self.value) < 1


#   def _is_under_char_limit(self):
#     return len(self.value) <= self.max_chars

#   def _is_valid_input(self):
#     try:
#       ipaddress.IPv4Address(self.value)
#       return True
#     except ValueError:
#       return False

#   def _validate_input(self):
#     if self._is_valid_input() and not self.input_empty:
#       self.input_error = False
#     else:
#       self.input_error = True


#   def update(self):
#     for key in self.valid_inputs.keys():
#       if pyxel.btnp(key) and self._is_under_char_limit():
#         self.value += self.valid_inputs[key]
#         self._validate_input()

#     if pyxel.btnp(pyxel.KEY_BACKSPACE):
#       self.value = self.value[0:len(self.value) - 1]
#       self._validate_input()


#     if pyxel.btnp(pyxel.KEY_ENTER):
#       print("Submit attempted:\t{}".format(self.value))
#       if not self.input_error:
#         self.input_submitted = True

#   def draw(self):
#     pyxel.rect(self.x, self.y, self.width, self.height, 4)
#     pyxel.text(self.x + 6, self.y + 2, self.value, self.text_color if not self.input_error else 8)

#     if self.input_error:
#       pyxel.text(self.x, self.y + self.height + 2, "Invalid IP Address", 8)

#     if self.input_empty:
#       pyxel.text(self.x + 12, self.y + 2, "IPv4 Address", self.text_color)


#   def reset(self):
#     self.value = ''

import pyxel
import constants

from label import ray_label, key_cap_label


class ReplayMenu():
  def __init__(self):
    self.menu_width = 90
    self.menu_height = 30
    self.options = ["REMATCH", "RETURN TO MENU"]
    self.option_padding = 10
    self.labels = []
    self.selected_colors = (6, 7)
    self.deselected_colors = (12, 13)
    self.active_option = 0
    self.selection = None

    # TODO: center text in menu
    total_height = (len(self.options) - 1) * self.option_padding
    x = constants.GAME_WIDTH * .5
    y = (constants.GAME_HEIGHT * .65) + (self.menu_height * .5 - total_height)
    for option in self.options:
      self.labels.append(ray_label.RayLabel(text=option, size=4.0, origin=(x, y), alignment=ray_label.Alignment.CENTER))
      y += self.option_padding

  def update_active_option(self, direction):
    if direction > 0:
      if self.active_option == 0:
        self.active_option = len(self.options) - 1
      else:
        self.active_option -= 1
    else:
      if self.active_option == len(self.options) - 1:
        self.active_option = 0
      else:
        self.active_option += 1


  def update(self):
    if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
      self.update_active_option(1)

    elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
      self.update_active_option(-1)

    elif pyxel.btnp(pyxel.KEY_ENTER):
      self.selection = self.options[self.active_option]

  def draw(self):
    # draw rect
    pyxel.rect(constants.GAME_WIDTH * .5 - self.menu_width * .5, constants.GAME_HEIGHT * .65, self.menu_width, self.menu_height, col=0)
    # draw border
    pyxel.rectb(constants.GAME_WIDTH * .5 - self.menu_width * .5, constants.GAME_HEIGHT * .65, self.menu_width, self.menu_height, col=12)
    # draw labels
    for i, label in enumerate(self.labels):
      colors = self.selected_colors if i == self.active_option else self.deselected_colors
      label.draw(colors)



import pyxel
import constants
from label import menu_option_label, ray_label


class SelectionMenu:
  def __init__(self, primary_options, secondary_options=[], option_padding=0, options_padding=0):
    self.labels = []
    self.options = primary_options + secondary_options
    self.primary_options = primary_options
    self.secondary_options = secondary_options
    self.option_padding = option_padding
    self.options_padding = options_padding
    self.active_option = 0
    self.selection = None

    total_height = (len(self.primary_options) - 1) * option_padding
    if secondary_options:
      total_height += (len(self.secondary_options) - 1) * option_padding + options_padding
    x = constants.GAME_WIDTH / 2
    y = (constants.GAME_HEIGHT - total_height) / 2
    for i, option in enumerate(self.options):
      if i == len(self.primary_options):
        y += options_padding
      self.labels.append(menu_option_label.MenuOptionLabel(text=option, size=4.0, origin=(x, y), alignment=ray_label.Alignment.CENTER))
      y += option_padding

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

    for i, label in enumerate(self.labels):
      if i == self.active_option:
        label.select()
      else:
        label.deselect()

  def draw(self):
    for label in self.labels:
      label.draw()



    # for option in self.primary_options:
    #   pyxel.text(x, y, option, 6 if option == self.active_option else 12)
    #   y += self.option_padding

    # y += self.options_padding

    # for option in self.secondary_options:
    #   pyxel.text(x, y, option, 6 if option == self.active_option else 12)
    #   y += self.option_padding

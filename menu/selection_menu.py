import pyxel


class SelectionMenu:
  def __init__(self, x, y, primary_options, secondary_options=[], option_padding=0, options_padding=0):
    self.x = x
    self.y = y
    self.options = primary_options + secondary_options
    self.primary_options = primary_options
    self.secondary_options = secondary_options
    self.option_padding = option_padding
    self.options_padding = options_padding
    self.active_option = primary_options[0]
    self.selection = None
    self.option_labels = []

  def update_active_option(self, direction):
    active_option_idx = self.options.index(self.active_option)
    if direction > 0:
      if active_option_idx == 0:
        self.active_option = self.options[-1]
      else:
        self.active_option = self.options[active_option_idx - 1]
    else:
      if active_option_idx == len(self.options) - 1:
        self.active_option = self.options[0]
      else:
        self.active_option = self.options[active_option_idx + 1]

  def update(self):
    if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
      self.update_active_option(1)

    elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
      self.update_active_option(-1)

    elif pyxel.btnp(pyxel.KEY_ENTER):
      print("A selection was made")
      self.selection = self.active_option

  def draw(self):
    x = self.x
    y = self.y

    for option in self.primary_options:
      pyxel.text(x, y, option, 6 if option == self.active_option else 12)
      y += self.option_padding

    y += self.options_padding

    for option in self.secondary_options:
      pyxel.text(x, y, option, 6 if option == self.active_option else 12)
      y += self.option_padding

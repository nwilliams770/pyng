import pyxel
from . import ray_label

class KeyCapLabel(object):
  def __init__(self, key_str, key_code, key_padding=5.0, size=5.0, unpressed_colors=(12, 13), pressed_colors=(6, 7), origin=(0, 0), alignment=ray_label.Alignment.LEFT):
    self.key_padding = key_padding
    self.unpressed_colors = unpressed_colors
    self.pressed_colors = pressed_colors
    self.key_code = key_code
    self._label = ray_label.RayLabel(text=key_str, size=size, origin=origin, alignment=alignment)

  @property
  def width(self):
    return self._label.width + self.key_padding * 2

  @property
  def height(self):
    return self._label.height + self.key_padding * 2

  def draw(self):
    colors = self.pressed_colors if pyxel.btn(self.key_code) else self.unpressed_colors
    x = self._label.left - self.key_padding
    y = self._label.top - self.key_padding
    w = self.width
    h = self.height

    pyxel.rectb(x, y, w, h, col=colors[0])
    self._label.draw(colors)



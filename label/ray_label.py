import pyxel
import yaml
import math
import os


class Alignment:
  LEFT = 1
  CENTER = 2
  RIGHT = 3


class Typeface:
  NORMAL = 'normal.yaml'
  ULTRAWIDE = 'ultrawide.yaml'  # TODO
  NARROW = 'narrow.yaml'  # TODO


class RayLabel(object):
  def __init__(self, text, typeface=Typeface.NORMAL, size=10.0, colors=(2, 3), origin=(0, 0), alignment=Alignment.LEFT):
    self.text = self._format(text)
    self.typeface = typeface
    self.size = float(size)
    self.colors = colors
    self.origin = origin
    self.alignment = alignment
    _font_cache.load(typeface)

    self._glyphs = [_font_cache.get_glyph(character=c, typeface=typeface, size=size) for c in self.text]

    # Compute the width of the label
    self._width = 0
    for glyph in self._glyphs:
      self._width += math.ceil(glyph.size[0] + glyph.kerning)
    self._width -= glyph.kerning
    self._height = max([g.size[1] for g in self._glyphs])

    #  Note where we should draw from based on text alignment
    if alignment == Alignment.LEFT:
      self._left_origin_x = self.origin[0]
    elif alignment == Alignment.CENTER:
      self._left_origin_x = self.origin[0] - self._width / 2
    elif alignment == Alignment.RIGHT:
      self._left_origin_x = self.origin[0] - self._width

  @property
  def width(self):
    return self._width

  @property
  def height(self):
    return self._height

  def draw(self, colors=None):
    # Draw, offset to account for alignment
    x = self._left_origin_x
    y = self.origin[1] - self._height / 2

    colors = colors or self.colors

    for glyph in self._glyphs:
      glyph.draw(colors=colors, origin=(x, y))
      x += math.ceil(glyph.size[0] + glyph.kerning)

  def _format(self, text):
    """Removes illegal characters"""
    text = text.upper()
    return text


class Glyph(object):
  def __init__(self, lines, size, kerning):
    self.lines = lines
    self.size = size
    self.kerning = kerning

  def draw(self, colors, origin):
    all_points = set()
    bright_points = set()

    for (ax, ay), (bx, by) in self.lines:
      a = (origin[0] + ax, origin[1] + ay)
      b = (origin[0] + bx, origin[1] + by)
      pyxel.line(a[0], a[1], b[0], b[1], colors[0])

      if a in all_points:
        bright_points.add(a)
      if b in all_points:
        bright_points.add(b)

      all_points.add(a)
      all_points.add(b)

    for p in bright_points:
      pyxel.pset(p[0], p[1], colors[1])


class FontCache(object):
  def __init__(self):
    self._typeface_cache = {}
    self._glyph_cache =  {}

  def load(self, typeface):
    if typeface in self._typeface_cache:
      return

    with open(os.path.join(os.path.dirname(__file__), typeface), 'r') as f:
      self._typeface_cache[typeface] = yaml.safe_load(f)

  def get_glyph(self, character, typeface, size):
    if (character, typeface, size) not in self._glyph_cache:
      if character not in self._typeface_cache[typeface]['glyphs']:
        return Glyph(lines=[], size=(0, 0), kerning=0)
        raise ValueError(f"This typeface does not support the character '{character}'")

      settings = self._typeface_cache[typeface]['settings']
      glyph_lines = self._typeface_cache[typeface]['glyphs'][character]

      kerning = max(2, size * settings['kerning'])  # ensure there's always a blank pixel between glyphs
      scale_x = size * settings['scale_to_size_one'][0]
      scale_y = size * settings['scale_to_size_one'][1]
      glyph_size = (settings['unit_glyph_size'][0] * size, settings['unit_glyph_size'][1] * size)

      lines = []
      for (ax, ay), (bx, by) in glyph_lines:
        ax = float(ax) * scale_x
        ay = float(ay) * scale_y
        bx = float(bx) * scale_x
        by = float(by) * scale_y
        lines.append(((ax, ay), (bx, by)))

      glyph = Glyph(lines=lines, size=glyph_size, kerning=kerning)
      self._glyph_cache[(character, typeface, size)] = glyph

    return self._glyph_cache[(character, typeface, size)]


_font_cache = FontCache()

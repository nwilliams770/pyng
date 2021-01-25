import pyxel
from . import ray_label

class MenuOptionLabel(object):
    def __init__(self, text, size=6.0, deselected_colors=(12,  13), selected_colors=(1, 1), underline_color=6, origin=(0, 0), alignment=ray_label.Alignment.LEFT):
        self._label = ray_label.RayLabel(text=text, size=size, origin=origin, alignment=alignment)
        self.deselected_colors = deselected_colors
        self.selected_colors = selected_colors
        self.underline_color = underline_color
        self._size = size
        self._selected = False
        self._anim_left = True

    @property
    def is_selected(self):
        return self._selected

    def select(self):
        self._selected = True
        self._label.set_size(self._size * 1.2)

    def deselect(self):
        self._selected = False
        self._label.set_size(self._size)

    def draw(self):
        color =  self.selected_colors if self.is_selected else self.deselected_colors
        self._label.draw(color)

        if self.is_selected:
            # draw an underline bouncing back and forth on selected labels
            y = self._label.bottom + 5
            x_min = self._label.left
            x_max = self._label.left + self._label.width

            w = min(self._label.width, 20)
            max_start = x_max - x_min - w
            speed = self._label.width / 10.0
            step = ((speed * pyxel.frame_count) % max_start)
            if self._anim_left:
                start = x_min + step

                # If we high the right edge, bounce back
                if start + w >= x_max - speed:
                    self._anim_left = False
            else:
                start = x_min + max_start - step

                # if we hit  the lleft edge, bounce
                if start <= x_min + speed:
                    self._anim_left = True

            pyxel.line(start, y, start + w, y, col=self.underline_color)

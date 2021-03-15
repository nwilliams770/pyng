import pyxel
import constants

from label import ray_label, key_cap_label


class CreditsScreen():
  def __init__(self):
    self.navigate_to_menu = None
    self.title = ray_label.RayLabel("CREDITS", size=8.0, colors=(1, 1), origin=(constants.GAME_WIDTH * .5, 10), alignment=ray_label.Alignment.CENTER)

    self.label_a = ray_label.RayLabel("The One and Only...", size=6.0, colors=(2, 3), origin=(constants.GAME_WIDTH * .5, 50), alignment=ray_label.Alignment.CENTER)
    self.label_b = ray_label.RayLabel("Gala Oksenhorn", size=10.0, colors=(4, 5), origin=(constants.GAME_WIDTH * .5, 64), alignment=ray_label.Alignment.CENTER)

    self.footer_label = ray_label.RayLabel("Return to Main Menu", size=4.0, colors=(12, 13), origin=(constants.GAME_WIDTH * .5 + 13, 178), alignment=ray_label.Alignment.CENTER)
    self.footer_key_cap = key_cap_label.KeyCapLabel(key_str="M", key_code=pyxel.KEY_M, size=4.0, origin=(constants.GAME_WIDTH * .5 - 47, self.footer_label.top + 2), alignment=ray_label.Alignment.CENTER)

  def update(self):
    if pyxel.btnp(self.footer_key_cap.key_code):
      self.navigate_to_menu = True

  def draw(self):
    self.title.draw()
    self.label_a.draw()
    self.label_b.draw()
    self.footer_label.draw()
    self.footer_key_cap.draw()

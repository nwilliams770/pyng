import pyxel
import constants

from label import ray_label, key_cap_label


class AIMenu():
  def __init__(self):
    self.navigate_to_menu = None
    self.title = ray_label.RayLabel("COMING SOON", size=12.0, colors=(1, 1), origin=(constants.GAME_WIDTH * .5, constants.GAME_HEIGHT * .5 - 10), alignment=ray_label.Alignment.CENTER)

    self.footer_label = ray_label.RayLabel("Return to Main Menu", size=4.0, colors=(12, 13), origin=(constants.GAME_WIDTH * .5 + 13, 178), alignment=ray_label.Alignment.CENTER)
    self.footer_key_cap = key_cap_label.KeyCapLabel(key_str="M", key_code=pyxel.KEY_M, size=4.0, origin=(constants.GAME_WIDTH * .5 - 47, self.footer_label.top + 2), alignment=ray_label.Alignment.CENTER)

  def update(self):
    if pyxel.btnp(self.footer_key_cap.key_code):
      self.navigate_to_menu = True

  def draw(self):
    self.title.draw()
    self.footer_label.draw()
    self.footer_key_cap.draw()

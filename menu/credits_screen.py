import pyxel
import constants

from label import ray_label, key_cap_label

# TODO: Two AIs playing at super speed
class CreditsScreen():
  def __init__(self):
    self.navigate_to_menu = None
    self.title = ray_label.RayLabel("CREDITS", size=8.0, colors=(1, 1), origin=(constants.GAME_WIDTH / 2, 10), alignment=ray_label.Alignment.CENTER)
    self.footer_label = ray_label.RayLabel("Return to Main Menu:", size=4.0, colors=(12, 13), origin=(constants.GAME_WIDTH / 2, 168), alignment=ray_label.Alignment.CENTER)
    self.footer_key_cap = key_cap_label.KeyCapLabel(key_str="M", key_code=pyxel.KEY_M, size=4.0, origin=(constants.GAME_WIDTH / 2, self.footer_label.bottom + 11), alignment=ray_label.Alignment.CENTER)

  def update(self):
    if pyxel.btnp(self.footer_key_cap.key_code):
      self.navigate_to_menu = True

  def draw(self):
    self.title.draw()
    self.footer_label.draw()
    self.footer_key_cap.draw()

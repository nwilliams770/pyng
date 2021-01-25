import pyxel
import constants

from label import ray_label

# TODO: Two AIs playing at super speed
class CreditsScreen():
  def __init__(self):
    self.title = ray_label.RayLabel("CREDITS MENU", size=16, colors=(1, 1), origin=(constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 2), alignment=ray_label.Alignment.CENTER)
    self.enter_key_label = ray_label.RayLabel('PRESS ENTER TO RETURN TO MENU', size=6, colors=(1, 1), origin=(constants.GAME_WIDTH / 2, constants.GAME_HEIGHT * 0.75), alignment=ray_label.Alignment.CENTER)
    self.navigate_to_menu = None

  def update(self):
    if pyxel.btnp(pyxel.KEY_ENTER):
      self.navigate_to_menu = True

  def draw(self):
    self.title.draw()
    self.enter_key_label.draw()

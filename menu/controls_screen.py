import pyxel
import constants

from label import ray_label

# TODO: Just draw the key caps for P1 and P2, as well as how many points to win
# TODO: maybeeee, have p1 and p2 paddles, if p1 controls hit, key cap lights up or something like thats


class ControlsScreen():
  def __init__(self):
    self.title = ray_label.RayLabel("HIT BALLS, BIG FUN", size=16, colors=(1, 1), origin=(constants.GAME_WIDTH / 2, constants.GAME_HEIGHT / 2), alignment=ray_label.Alignment.CENTER)
    self.enter_key_label = ray_label.RayLabel('PRESS ENTER TO RETURN TO MENU', size=6, colors=(1, 1), origin=(constants.GAME_WIDTH / 2, constants.GAME_HEIGHT * 0.75), alignment=ray_label.Alignment.CENTER)
    self.navigate_to_menu = None

  def update(self):
    if pyxel.btnp(pyxel.KEY_ENTER):
      self.navigate_to_menu = True

  def draw(self):
    self.title.draw()
    self.enter_key_label.draw()

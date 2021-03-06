import pyxel
import constants

from label import ray_label, key_cap_label
from match.constants import *


class ControlsScreen():
  def __init__(self):
    self.p1_paddle = Paddle(player_num=1)
    self.p2_paddle = Paddle(player_num=2)

    self.p1_title = ray_label.RayLabel("Player One", size=6.0, colors=(1, 1), origin=(constants.GAME_WIDTH * .25, 25), alignment=ray_label.Alignment.CENTER)
    self.p2_title = ray_label.RayLabel("Player Two", size=6.0, colors=(1, 1), origin=(constants.GAME_WIDTH * .75, 25), alignment=ray_label.Alignment.CENTER)

    self.p1_up_key_cap = key_cap_label.KeyCapLabel(key_str="Q", key_code=pyxel.KEY_Q, size=4.0, origin=(self.p1_title.left, 42), alignment=ray_label.Alignment.LEFT)
    self.p1_up_label = ray_label.RayLabel("Up", size=4.0, colors=(1, 1), origin=(self.p1_title.left + self.p1_up_key_cap.width, 42), alignment=ray_label.Alignment.LEFT)
    self.p2_up_key_cap = key_cap_label.KeyCapLabel(key_str="O", key_code=pyxel.KEY_O, size=4.0, origin=(self.p2_title.left, 42), alignment=ray_label.Alignment.LEFT)
    self.p2_up_label = ray_label.RayLabel("Up", size=4.0, colors=(1, 1), origin=(self.p2_title.left + self.p2_up_key_cap.width, 42), alignment=ray_label.Alignment.LEFT)

    self.p1_down_key_cap = key_cap_label.KeyCapLabel(key_str="A", key_code=pyxel.KEY_A, size=4.0, origin=(self.p1_title.left, 62), alignment=ray_label.Alignment.LEFT)
    self.p1_down_label = ray_label.RayLabel("Down", size=4.0, colors=(1, 1), origin=(self.p1_title.left + self.p1_down_key_cap.width, 62), alignment=ray_label.Alignment.LEFT)
    self.p2_down_key_cap = key_cap_label.KeyCapLabel(key_str="L", key_code=pyxel.KEY_L, size=4.0, origin=(self.p2_title.left, 62), alignment=ray_label.Alignment.LEFT)
    self.p2_down_label = ray_label.RayLabel("Down", size=4.0, colors=(1, 1), origin=(self.p2_title.left + self.p2_up_key_cap.width, 62), alignment=ray_label.Alignment.LEFT)

    self.win_condition_label = ray_label.RayLabel(f"First to {WIN_SCORE} points wins!", size=4.0, colors=(2, 3), origin=(constants.GAME_WIDTH * .5, 114), alignment=ray_label.Alignment.CENTER)
    self.footer_label = ray_label.RayLabel("Return to Main Menu", size=4.0, colors=(12, 13), origin=(constants.GAME_WIDTH * .5 + 13, 178), alignment=ray_label.Alignment.CENTER)
    self.footer_key_cap = key_cap_label.KeyCapLabel(key_str="M", key_code=pyxel.KEY_M, size=4.0, origin=(constants.GAME_WIDTH * .5 - 47, self.footer_label.top + 2), alignment=ray_label.Alignment.CENTER)
    self.navigate_to_menu = None

  def update(self):
    if pyxel.btnp(self.footer_key_cap.key_code):
      self.navigate_to_menu = True

    self.p1_paddle.update()
    self.p2_paddle.update()

  def draw(self):
    self.p1_title.draw()
    self.p2_title.draw()
    self.p1_up_key_cap.draw()
    self.p1_up_label.draw()
    self.p2_up_key_cap.draw()
    self.p2_up_label.draw()
    self.p1_down_key_cap.draw()
    self.p1_down_label.draw()
    self.p2_down_key_cap.draw()
    self.p2_down_label.draw()
    self.win_condition_label.draw()
    self.footer_label.draw()
    self.footer_key_cap.draw()
    self.p1_paddle.draw()
    self.p2_paddle.draw()

class Paddle:
  def __init__(self, player_num):
    self.player_num = player_num
    self.width = 2
    self.height = 16
    self.y = 106
    self.x = 40 if player_num == 1 else constants.GAME_WIDTH - 40 - self.width
    self.PLAYER_SPEED = 2

  def update(self):
    if self.player_num == 1:
      if pyxel.btn(pyxel.KEY_Q):
        self.update_player_pos(-self.PLAYER_SPEED)
      elif pyxel.btn(pyxel.KEY_A):
        self.update_player_pos(self.PLAYER_SPEED)
    elif self.player_num == 2:
      if pyxel.btn(pyxel.KEY_O):
        self.update_player_pos(-self.PLAYER_SPEED)
      elif pyxel.btn(pyxel.KEY_L):
        self.update_player_pos(self.PLAYER_SPEED)

  def update_player_pos(self, dy):
    if dy > 0:
      if self.y + self.height + dy <= 160:
        self.y += dy
      elif self.y + self.height + dy >= 160:
        self.y = 160 - self.height

    if dy < 0:
      if self.y + dy >= 80:
        self.y += dy
      elif self.y + dy <= 80:
        self.y = 80

  def draw(self):
    pyxel.rect(self.x, self.y, self.width, self.height, col=1)

"""
Responsible for the Pong Game Engine
"""

# TODOS:
# - Add game over logic
# - Add error state if too many dropped frames
# - Add options to game over to play again or go to menu
# - Style board
# - Potentially look into collision detection?


import pyxel
import random
import math

from match import match_type
from match.constants import *


class Engine():
  def __init__(self):
    self.ball = Ball()
    self.ball.alive = False
    self.player_one = Player(player_num=1)
    self.player_two = Player(player_num=2)
    self.post_score_delay = PRE_START_FRAME_DELAY
    self.last_scorer = None

  def update(self, p1_input, p2_input):
    self.update_match(p1_input, p2_input)
    return {
      'phase': 'playing',
      'p1_y': self.player_one.frame.y,
      'p1_score': self.player_one.score,
      'p2_y': self.player_two.frame.y,
      'p2_score': self.player_two.score,
      'ball_xy': (self.ball.frame.x, self.ball.frame.y),
      'ball_alive': self.ball.alive,
    }

  def update_match(self, p1_input, p2_input):
    if self.check_and_process_score():
      self.ball.alive = False

    self.player_one.update(p1_input)
    self.player_two.update(p2_input)

    if self.post_score_delay > 0:
      self.post_score_delay -= 1
      if self.post_score_delay == 0:
        self.ball.reset(self.last_scorer)
    else:
      if self.player_one.frame.intersects(self.ball.frame):
        (new_dx, new_dy) = self.ball.handle_player_collision(self.player_one)
        self.ball.update_trajectory(new_dx, new_dy)
      elif self.player_two.frame.intersects(self.ball.frame):
        (new_dx, new_dy) = self.ball.handle_player_collision(self.player_two)
        self.ball.update_trajectory(new_dx, new_dy)
      elif self.ball.hit_top_wall() or self.ball.hit_bottom_wall():
        self.ball.update_trajectory(self.ball.dx, -self.ball.dy)

      self.ball.update()

  def check_for_winner(self):
    if self.player_one.score == WIN_SCORE:
      return self.player_one.player_num
    elif self.player_two.score == WIN_SCORE:
      return self.player_two.player_num
    else:
      return None

  def check_and_process_score(self):
    if self.ball.alive == False:
      return False

    if self.ball.hit_left_wall():
      self.player_two.score += 1
      self.last_scorer = 2
    elif self.ball.hit_right_wall():
      self.player_one.score += 1
      self.last_scorer = 1
    else:
      return False

    self.post_score_delay = PRE_START_FRAME_DELAY
    return True


class Rect:
  def __init__(self, x=0, y=0, width=0, height=0):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

  @property
  def left(self):
    return self.x

  @property
  def right(self):
    return self.x + self.width

  @property
  def top(self):
    return self.y

  @property
  def bottom(self):
    return self.y + self.height

  def intersects(self, rect):
    if (self.right >= rect.left and self.left <= rect.right) and (self.top <= rect.bottom and self.bottom >= rect.top):
      return True
    else:
      return False


class Player:
  def __init__(self, player_num):
    self.player_num = player_num
    self.score = 0
    initial_x_pos = PLAYER_1_X if player_num == 1 else PLAYER_2_X
    initial_y_pos = 10 if player_num == 1 else COURT_HEIGHT - 10 - PLAYER_HEIGHT
    self.frame = Rect(x=initial_x_pos, y=initial_y_pos, width=PLAYER_WIDTH, height=PLAYER_HEIGHT)

  @property
  def moving_up(self):
    key_up = pyxel.KEY_Q if self.player_num == 1 else pyxel.KEY_I
    return pyxel.btn(key_up)

  @property
  def moving_down(self):
    key_down = pyxel.KEY_A if self.player_num == 1 else pyxel.KEY_K
    return pyxel.btn(key_down)

  def update(self, key_input):
    if self.player_num == 1:
      if key_input == pyxel.KEY_Q:
        self.update_player_pos(-PLAYER_SPEED)
      elif key_input == pyxel.KEY_A:
        self.update_player_pos(PLAYER_SPEED)
    elif self.player_num == 2:
      if key_input == pyxel.KEY_O:
        self.update_player_pos(-PLAYER_SPEED)
      elif key_input == pyxel.KEY_L:
        self.update_player_pos(PLAYER_SPEED)

  def update_player_pos(self, dy):
    if dy > 0:
      if self.frame.bottom + dy <= COURT_HEIGHT:
        self.frame.y += dy
      elif self.frame.bottom + dy >= COURT_HEIGHT:
        self.frame.y = COURT_HEIGHT - self.frame.height

    if dy < 0:
      if self.frame.top + dy >= 0:
        self.frame.y += dy
      elif self.frame.top + dy <= 0:
        self.frame.y = 0


class Ball:
  def __init__(self):
    self.frame = Rect(width=BALL_WIDTH, height=BALL_WIDTH)
    self.reset()

  def update(self):
    self.frame.x += self.dx
    self.frame.y += self.dy

  def reset(self, last_scorer=None):
    rand_dx = 2 if random.randint(0, 1) else -2
    self.alive = True
    self.frame.x = COURT_WIDTH / 2
    self.frame.y = COURT_HEIGHT - 1 - self.frame.width if random.randint(0, 1) else 1
    self.dx = 1 if last_scorer == 1 else (-1 if last_scorer == 2 else rand_dx)
    self.dy = 2 if self.frame.y == 1 else -2

  def handle_player_collision(self, player):
    # Determine where paddle hit ball, top, middle, or bottom
    new_dx = -self.dx
    new_dy = self.dy

    distance_to_mid_paddle = round(self.frame.bottom - (player.frame.y + player.frame.height / 2))

    if -2 <= distance_to_mid_paddle <= 2:
      new_dy = 0
    # ball hit upper region of paddle
    elif distance_to_mid_paddle < 0 and distance_to_mid_paddle < -1:
      new_dy = -abs(self.dy) if self.dy != 0 else -2
    # ball hit lower region of paddle
    elif distance_to_mid_paddle > 0 and distance_to_mid_paddle > 1:
      new_dy = abs(self.dy) if self.dy != 0 else 2

    new_dy = self.handle_potential_spin(new_dy, player)

    return (new_dx, new_dy)

  def handle_potential_spin(self, dy, player):
    if 1 < dy < 3 or -3 < dy < -1:
      if player.moving_up:
        dy = -1 if dy < 0 else 3
      if player.moving_down:
        dy = 1 if dy > 0 else -3

    return dy

  def update_trajectory(self, dx, dy):
    self.dx = dx
    self.dy = dy

  def hit_left_wall(self):
    return self.frame.x <= 0

  def hit_right_wall(self):
    return self.frame.x + self.frame.width >= COURT_WIDTH

  def hit_player_paddle(self, p1x, p1y, p2x, p2y):
    hit_p1 = self.frame.x <= p1x + PLAYER_WIDTH and p1y <= self.frame.y <= p1y + PLAYER_HEIGHT + self.frame.width
    hit_p2 = self.frame.x >= p2x - PLAYER_WIDTH and p2y <= self.frame.y <= p2y + PLAYER_HEIGHT + self.frame.width
    return hit_p1 or hit_p2

  def hit_top_wall(self):
    return self.frame.y <= 0

  def hit_bottom_wall(self):
    return self.frame.y + self.frame.height >= COURT_HEIGHT

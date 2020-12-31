"""
A 1-on-1 game instance

Should update or draw from state in ALL game cases?
  -- Always draw from state, regardless of game mode


"""

import pyxel
import random
import math

from match import match_type


COURT_WIDTH = 140
COURT_HEIGHT = 105


class Match():
  def __init__(self, match_type):
    self.match_type = match_type

    self.should_close = False

    self.state = None
    self.is_primary = True  # TODO - base this off match_type
    self.multiplayer = None  # TODO - grab this from match_type if it exists

    if self.is_primary:
      self.ball = Ball()
      self.ball.alive = False
      self.player_one = Player(player_num=1)
      self.player_two = Player(player_num=2)
      self.post_score_delay = PRE_START_FRAME_DELAY
      self.last_scorer = None

  # MODEL

  @property
  def game_over(self):
    return False

  def update(self):
    if self.is_primary:
      self.update_as_primary()
    else:
      self.update_as_secondary()

  def update_as_primary(self):
    p1_input, p2_input = self.get_inputs()
    self.update_match(p1_input, p2_input)
    self.state = self.capture_state()
    # self.multiplayer.send(state) TODO

  def capture_state(self):
    return {
      'state': 'playing', # countdown, playing, end
      'p1_y': self.player_one.frame.y,
      'p1_score': self.player_one.score,
      'p2_y': self.player_two.frame.y,
      'p2_score': self.player_two.score,
      'ball_xy': (self.ball.frame.x, self.ball.frame.y),
      'ball_alive': self.ball.alive,
    }

  def update_as_secondary(self):
    # state = self.multiplayer.get_message() TODO
    # draw_from_state(state)
    # keys_pressed = TODO
    # self.multiplayer.send_message({'keys': keys_pressed})
    pass

  # PRIMARY

  def get_inputs(self):
    p1_input = None
    p2_input = None

    is_p1_local = True  # For now, even over LAN, p1 is always the primary
    is_p2_local = not isinstance(self.match_type, match_type.LANMultiplayer)

    if is_p1_local:
      if pyxel.btn(pyxel.KEY_W) and pyxel.btn(pyxel.KEY_S):
        p1_input = None
      elif pyxel.btn(pyxel.KEY_W):
        p1_input = pyxel.KEY_W
      elif pyxel.btn(pyxel.KEY_S):
        p1_input = pyxel.KEY_S
    else:
      # We should never get here with the current assumption that p1 is always primary
      pass

    if is_p2_local:
      if pyxel.btn(pyxel.KEY_O) and pyxel.btn(pyxel.KEY_L):
        p2_input = None
      elif pyxel.btn(pyxel.KEY_O):
        p2_input = pyxel.KEY_O
      elif pyxel.btn(pyxel.KEY_L):
        p2_input = pyxel.KEY_L
    else:
      pass # TODO get secondary input over the wire

    return (p1_input, p2_input)

  def update_match(self, p1_input, p2_input):
    if self.check_for_score():
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

  def check_for_score(self):
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

  def draw(self):
    if not self.state:
      return

    draw_from_state(self.state)








def draw_from_state(state):
  pyxel.rect(0, 0, COURT_WIDTH, COURT_HEIGHT, COURT_COLOR)

  for i in range(0, COURT_HEIGHT, 3):
    pyxel.rect((COURT_WIDTH / 2 - COURT_TICK_WIDTH / 2), i, COURT_TICK_WIDTH, COURT_TICK_HEIGHT, COURT_TICK_COLOR)

  # TODO - center these
  pyxel.text(COURT_WIDTH / 2 - 20, 10, str(state['p1_score']), 11)
  pyxel.text(COURT_WIDTH / 2 + 16, 10, str(state['p2_score']), 11)

  pyxel.rect(PLAYER_1_X, state['p1_y'], PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)
  pyxel.rect(PLAYER_2_X, state['p2_y'], PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)

  if state['ball_alive']:
    ball_x, ball_y = state['ball_xy']
    pyxel.rect(ball_x, ball_y, BALL_WIDTH, BALL_WIDTH, BALL_COLOR)


COURT_COLOR = 0
COURT_TICK_WIDTH = 1
COURT_TICK_HEIGHT = 2
COURT_TICK_COLOR = 7

PLAYER_WIDTH = 2
PLAYER_HEIGHT = 10
PLAYER_1_X = 10
PLAYER_2_X = COURT_WIDTH - 10 - PLAYER_WIDTH

PLAYER_SPEED = 2
PLAYER_COLOR = 11

BALL_WIDTH = 1
BALL_COLOR = 11

PRE_START_FRAME_DELAY = 60

# To-do:
# - Scoring, match start/stop, game complete
# - Add quit key to init func
# - accelerating paddles?
# - styling, intro screen, gameover text
# - networking
# - comet trail on ball?

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
    key_up = pyxel.KEY_W if self.player_num == 1 else pyxel.KEY_I
    return pyxel.btn(key_up)

  @property
  def moving_down(self):
    key_down = pyxel.KEY_S if self.player_num == 1 else pyxel.KEY_K
    return pyxel.btn(key_down)

  def update(self, key_input):
    if self.player_num == 1:
      if key_input == pyxel.KEY_W:
        self.update_player_pos(-PLAYER_SPEED)
      elif key_input == pyxel.KEY_S:
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

import pyxel
import random
import math

COURT_WIDTH = 140
COURT_HEIGHT = 105
COURT_COLOR = 0
COURT_TICK_WIDTH = 1
COURT_TICK_HEIGHT = 2
COURT_TICK_COLOR = 7

PLAYER_ONE = 'P1'
PLAYER_TWO = 'P2'
PLAYER_WIDTH = 2
# PLAYER_HEIGHT = 6
PLAYER_HEIGHT = 10
PLAYER_SPEED = 2
PLAYER_COLOR = 11

BALL_WIDTH = 1
BALL_INITAL_SPEED = 1
BALL_COLOR = 11

PRE_START_FRAME_DELAY = 60

# To-do:
# - Scoring, match start/stop, game complete
# - accelerating paddles
# - ball slowly increases speed
# - better collision detection - implement rect intersect func
# - styling, intro screen, gameover text
# - networking


class App:
  def __init__(self):
    self.match = None
    pyxel.init(COURT_WIDTH, COURT_HEIGHT, caption="Lan Pong", fps=30)
    pyxel.run(self.update, self.draw)

  def update(self):
    if not self.match:
      self.start_new_match()
    else:
      self.match.update()

  def draw(self):
    if self.match:
      self.match.draw()

  def start_new_match(self):
    self.match = Match()

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

class Match:
  def __init__(self):
    self.player_one = Player(player_num=1)
    self.player_two = Player(player_num=2)
    self.ball = Ball()
    self.p1_score = 0
    self.p2_score = 0
    self.post_score_delay = PRE_START_FRAME_DELAY
    self.last_scorer = None

  def update(self):
    if self.check_for_score():
      self.ball.alive = False

    self.player_one.update()
    self.player_two.update()

    if self.post_score_delay > 0:
      self.post_score_delay -= 1
      if self.post_score_delay == 0:
        self.ball.reset(self.last_scorer)
      return

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
      self.p2_score += 1
      self.last_scorer = PLAYER_TWO
    elif self.ball.hit_right_wall():
      self.p1_score += 1
      self.last_scorer = PLAYER_ONE
    else:
      return False

    self.post_score_delay = PRE_START_FRAME_DELAY
    return True

  def draw(self):
    self.draw_background()
    self.draw_scores()
    self.player_one.draw()
    self.player_two.draw()
    self.ball.draw()

  def draw_background(self):
    pyxel.rect(0, 0, COURT_WIDTH, COURT_HEIGHT, COURT_COLOR)

    for i in range(0, COURT_HEIGHT, 3):
      pyxel.rect((COURT_WIDTH / 2 - COURT_TICK_WIDTH / 2), i, COURT_TICK_WIDTH, COURT_TICK_HEIGHT, COURT_TICK_COLOR)

  def draw_scores(self):
    # Todo center these
      pyxel.text(COURT_WIDTH / 2 - 20, 10, str(self.p1_score), 11)
      pyxel.text(COURT_WIDTH / 2 + 16, 10, str(self.p2_score), 11)

class Player:
  def __init__(self, player_num):
    self.player_num = player_num
    initial_x_pos = 10 if player_num == 1 else COURT_WIDTH - 10
    initial_y_pos = 10 if player_num == 1 else COURT_HEIGHT - 10 - PLAYER_HEIGHT
    self.frame = Rect(x = initial_x_pos, y= initial_y_pos, width=PLAYER_WIDTH, height=PLAYER_HEIGHT)

  @property
  def moving_up(self):
    key_up = pyxel.KEY_W if self.player_num == 1 else pyxel.KEY_I
    return pyxel.btn(key_up)

  @property
  def moving_down(self):
    key_down = pyxel.KEY_S if self.player_num == 1 else pyxel.KEY_K
    return pyxel.btn(key_down)

  def update(self):
    if self.player_num == 1:
      if pyxel.btn(pyxel.KEY_W):
        self.update_player_pos(-PLAYER_SPEED)

      if pyxel.btn(pyxel.KEY_S):
        self.update_player_pos(PLAYER_SPEED)

    if self.player_num == 2:
      if pyxel.btn(pyxel.KEY_I):
        self.update_player_pos(-PLAYER_SPEED)

      if pyxel.btn(pyxel.KEY_K):
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


  def draw(self):
    pyxel.rect(self.frame.x, self.frame.y, self.frame.width, self.frame.height, PLAYER_COLOR)

class Ball:
  def __init__(self):
    self.frame = Rect(width=BALL_WIDTH, height=BALL_WIDTH)
    self.reset()

  def update(self):
    self.frame.x += self.dx
    self.frame.y += self.dy

  def draw(self):
    if self.alive:
      pyxel.rect(self.frame.x, self.frame.y, self.frame.width, self.frame.height, BALL_COLOR)

  def reset(self, last_scorer=None):
    rand_dx = 2 if random.randint(0, 1) else -2
    self.alive = True
    self.frame.x = COURT_WIDTH / 2
    self.frame.y = COURT_HEIGHT - 1 - self.frame.width if random.randint(0, 1) else 1
    self.dx = 1 if last_scorer == PLAYER_ONE else (-1 if last_scorer == PLAYER_TWO else rand_dx)
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

if __name__ == "__main__":
  App()

import pyxel

BG_WIDTH = 120
BG_HEIGHT = 80
BG_COLOR = 0
BG_PADDING = 2
BG_TICK_WIDTH = 1
BG_TICK_HEIGHT = 2
BG_TICK_COLOR = 7

PLAYER_WIDTH = 2
PLAYER_HEIGHT = 6
PLAYER_SPEED = 1
PLAYER_COLOR = 11

BALL_RADIUS = 2
BALL_INITAL_SPEED = 1.5
BALL_COLOR = 3


# Should app init function draw the BG, dividing line, player scores?
# Handles collision detection?
class App:
  def __init__(self):
    self.match = None
    pyxel.init(BG_WIDTH, BG_HEIGHT, caption="Lan Pong", fps=30)
    pyxel.run(self.update, self.draw)

  def update(self):
    if not self.match:
      self.start_new_match()
    else:
      self.match.update()

  def draw(self):
    pyxel.circ(1, 1, 20, 5)
    if self.match:
      self.match.draw()

  def start_new_match(self):
    self.match = Match()

class Match:
  def __init__(self):
    self.player_one = Player(1)
    self.player_two = Player(2)
    self.ball = Ball(BG_WIDTH / 2, BG_HEIGHT / 2)

  def update(self):
    self.player_one.update()
    self.player_two.update()

  def draw(self):
    self.draw_background()
    self.player_one.draw()
    self.player_two.draw()

  def draw_background(self):
    pyxel.rect(0, 0, BG_WIDTH, BG_HEIGHT, BG_COLOR)

    for i in range(BG_PADDING, BG_HEIGHT - BG_PADDING, 3):
      pyxel.rect((BG_WIDTH / 2 - BG_TICK_WIDTH / 2), i, BG_TICK_WIDTH, BG_TICK_HEIGHT, BG_TICK_COLOR)

# class Background:

class Player:
  def __init__(self, player_num):
    self.x = 10 if player_num == 1 else 70
    self.y = 20
    self.w = PLAYER_WIDTH
    self.h = PLAYER_HEIGHT
    self.player_num = player_num

  def update(self):
    if self.player_num == 1:
      if pyxel.btn(pyxel.KEY_W):
        self.update_player_pos(-PLAYER_SPEED)
        # self.y += PLAYER_SPEED

      if pyxel.btn(pyxel.KEY_S):
        self.update_player_pos(PLAYER_SPEED)
        # self.y -= PLAYER_SPEED


    if self.player_num == 2:
      if pyxel.btn(pyxel.KEY_I):
        self.update_player_pos(-PLAYER_SPEED)

      if pyxel.btn(pyxel.KEY_K):
        self.update_player_pos(PLAYER_SPEED)

  def update_player_pos(self, vector):
    print("vector", vector)
    if vector > 0:
      print("self.y", self.y, "BG_HEIGHT - BG_PADDING - PLAYER_HEIGHT", BG_HEIGHT - BG_PADDING - PLAYER_HEIGHT)
      if self.y + vector <= BG_HEIGHT - BG_PADDING - PLAYER_HEIGHT:
        self.y += vector

    if vector < 0:
      print("self.y", self.y, "BG_PADDING", BG_PADDING)
      if self.y + vector >= BG_PADDING:
        self.y += vector


  def draw(self):
    pyxel.rect(self.x, self.y, self.w, self.h, PLAYER_COLOR)


class Ball:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.r = BALL_RADIUS

  def update(self):
    pass

  def draw(self):
    pyxel.circ(self.x, self.y, self.r, BALL_COLOR)


if __name__ == "__main__":
  App()

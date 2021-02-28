import random
import math
import pyxel

from label import ray_label
import constants



class TitleScreen():
  def __init__(self):
    self.continue_to_selection = False
    self.balls = []
    for _ in range(10):
      self.balls.append(BouncingBall.random_ball())
    self.fireworks = []
    self.title_label = ray_label.RayLabel('PYNG', size=26, colors=(1, 1), origin=(constants.GAME_WIDTH * .5, constants.GAME_HEIGHT * .5), alignment=ray_label.Alignment.CENTER)
    self.enter_key_label = ray_label.RayLabel('PRESS ENTER TO START', size=6, colors=(1, 1), origin=(constants.GAME_WIDTH * .5, constants.GAME_HEIGHT * 0.75), alignment=ray_label.Alignment.CENTER)

  def update(self):
    self.update_balls()
    for firework in self.fireworks:
      firework.update()
    self.fireworks = [f for f in self.fireworks if not f.is_complete]

    if pyxel.btnp(pyxel.KEY_ENTER):
      self.continue_to_selection = True


  def draw(self):
    self.draw_balls()
    for firework in self.fireworks:
      firework.draw()

    self.title_label.draw()
    enter_key_label_colors = (2, 3) if pyxel.frame_count % 10 < 5 else (4, 5)
    self.enter_key_label.draw(colors=enter_key_label_colors)

  def update_balls(self):
    for ball in self.balls:
      if ball.x <= 0:
        ball.dx = -ball.dx
      elif ball.x >= constants.GAME_WIDTH:
        ball.dx = -ball.dx
      elif ball.y <= 0:
        if ball.dy < 0:
          ball.dy = -ball.dy
      elif ball.y >= constants.GAME_HEIGHT:
        ball.dy = -ball.dy

      ball.trail.insert(0, (ball.x, ball.y))
      while len(ball.trail) > 20:
        ball.trail.pop()

      ball.x += ball.dx
      ball.y += ball.dy
      ball.col = 1
      ball.trail_col = 12

    self.check_for_collisions()

  def check_for_collisions(self):
    balls_to_remove = []
    for i in range(len(self.balls)):
      for j in range(len(self.balls)):
        if i == j or i in balls_to_remove or j in balls_to_remove:
          continue

        if abs(self.balls[i].x - self.balls[j].x) <= 2 and abs(self.balls[i].y - self.balls[j].y) <= 5:
          balls_to_remove.append(i)
          balls_to_remove.append(j)
          self.fireworks.append(Firework(x=(self.balls[i].x + self.balls[j].x) // 2, y=(self.balls[i].y + self.balls[j].y) // 2))

    for ball_idx in balls_to_remove:
      self.balls[ball_idx] = BouncingBall.random_ball()


  def draw_balls(self):
    for ball in self.balls:
      pyxel.pset(ball.x, ball.y, ball.col)

      if len(ball.trail) >= 2:
        ptx, pty = ball.trail[0]
        for tx, ty in ball.trail:
          pyxel.line(ptx, pty, tx, ty, ball.trail_col)
          ptx = tx
          pty = ty

class BouncingBall:
  @staticmethod
  def random_ball():
      x, y = random.randint(0, 255), random.randint(0, 191)

      speed = 3.0
      angle = random.randint(0, 360) * math.pi / 180.0
      dx = speed * math.cos(angle)
      dy = speed * math.sin(angle)
      return BouncingBall(x, y, dx, dy)

  def __init__(self, x, y, dx, dy):
    self.x = x
    self.y = y
    self.dx = dx
    self.dy = dy
    self.trail = []
    self.col = 1
    self.trail_col = 12

class Firework:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.lifespan = 0
    self.angle = random.randint(0, 360) * math.pi / 180.0
    self.spokes = []
    self.speed = 5
    for i in range(6):
      angle = self.angle + ((360.0 * i / 6.0) * (math.pi / 180.0))
      if i % 2:
        length = float(random.randint(4, 12))
      else:
        length = float(random.randint(8, 18))
      self.spokes.append((angle, length))

  @property
  def is_complete(self):
    return self.lifespan >= 3 * self.speed

  def update(self):
    self.lifespan += 1

  def draw(self):
    for (angle, full_length) in self.spokes:
      if self.lifespan < self.speed:
        length = full_length * (self.lifespan / self.speed)
        yellow_endx = self.x + length * math.cos(angle)
        yellow_endy = self.y + length * math.sin(angle)
        pyxel.line(self.x, self.y, yellow_endx, yellow_endy, col=6)
      elif self.lifespan < 2 * self.speed:
        yellow_length = full_length * ((2 * self.speed - self.lifespan) / self.speed)
        red_length = full_length * ((self.lifespan - self.speed) / self.speed)
        yellow_startx = self.x + (full_length - yellow_length) * math.cos(angle)
        yellow_starty = self.y + (full_length - yellow_length) * math.sin(angle)
        joinx = self.x + full_length * math.cos(angle)
        joiny = self.y + full_length * math.sin(angle)

        red_endx = joinx + red_length * math.cos(angle)
        red_endy = joiny + red_length * math.sin(angle)

        pyxel.line(joinx, joiny, red_endx, red_endy, col=8)
        pyxel.line(yellow_startx, yellow_starty, joinx, joiny, col=6)
      else:
        red_length = full_length * ((3 * self.speed - self.lifespan ) / self.speed)
        red_startx = self.x + (2 * full_length - red_length) * math.cos(angle)
        red_starty = self.y + (2 * full_length - red_length) * math.sin(angle)

        red_endx = self.x + 2 * full_length * math.cos(angle)
        red_endy = self.y + 2 * full_length * math.sin(angle)

        pyxel.line(red_startx, red_starty, red_endx, red_endy, col=8)

import pyxel

from match.constants import *

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

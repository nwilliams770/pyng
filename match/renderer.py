import pyxel

from match.constants import *
from label import ray_label

def draw_from_state(state):
  pyxel.rect(0, 0, COURT_WIDTH, COURT_HEIGHT, COURT_COLOR)

  phase = state['phase']
  if phase == 'starting':
    render_starting(state)
  elif phase == 'playing':
    render_playing(state)


def render_playing(state):
    for i in range(0, COURT_HEIGHT, 8):
      pyxel.rect((COURT_WIDTH / 2 - COURT_TICK_WIDTH / 2), i, COURT_TICK_WIDTH, COURT_TICK_HEIGHT, COURT_TICK_COLOR)

    # TODO - center these
    pyxel.text(COURT_WIDTH / 2 - 20, 10, str(state['p1_score']), 11)
    pyxel.text(COURT_WIDTH / 2 + 16, 10, str(state['p2_score']), 11)

    pyxel.rect(PLAYER_1_X, state['p1_y'], PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)
    pyxel.rect(PLAYER_2_X, state['p2_y'], PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)

    if state['ball_alive']:
      ball_x, ball_y = state['ball_xy']
      pyxel.rect(ball_x, ball_y, BALL_WIDTH, BALL_WIDTH, BALL_COLOR)


def render_starting(state):
  frame = state['frame']
  starting_label_text = 'Starting in' if frame < 30 else '3' if frame < 60 else '2' if frame < 90 else '1'
  starting_label = ray_label.RayLabel(starting_label_text, size=16.0, colors=(1, 1), origin=(COURT_WIDTH / 2, 90), alignment=ray_label.Alignment.CENTER)
  starting_label.draw()

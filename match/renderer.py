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
  elif phase == 'end':
    render_end(state)


def render_starting(state):
  frame = state['frame']
  starting_label_text = 'Starting in' if frame < 30 else '3' if frame < 60 else '2' if frame < 90 else '1'
  starting_label = ray_label.RayLabel(starting_label_text, size=16.0, colors=(4, 5), origin=(COURT_WIDTH / 2, 90), alignment=ray_label.Alignment.CENTER)
  starting_label.draw()


def render_playing(state):
    _render_court()
    _render_score(state)
    _render_p1(state)
    _render_p2(state)

    if state['ball_alive']:
      _render_ball(state)


def render_end(state):
  _render_court()

  # Flash the scores
  if state['frame'] % 30.0 < 15:
    _render_score(state)

  if state['winner'] == 1:
    _render_p1(state)
  elif state['winner'] == 2:
    _render_p2(state)

  winner_x = (0.25 * COURT_WIDTH) if state['winner'] == 1 else (0.75 * COURT_WIDTH)
  winner_origin = (winner_x, COURT_HEIGHT / 2)
  label = ray_label.RayLabel(text="WINNER", size=8.0, origin=winner_origin, alignment=ray_label.Alignment.CENTER)
  label.draw()


def _render_court():
  for i in range(0, COURT_HEIGHT, 8):
    pyxel.rect((COURT_WIDTH / 2 - COURT_TICK_WIDTH / 2), i, COURT_TICK_WIDTH, COURT_TICK_HEIGHT, COURT_TICK_COLOR)


def _render_score(state):
  # TODO center these
  pyxel.text(COURT_WIDTH / 2 - 20, 10, str(state['p1_score']), 11)
  pyxel.text(COURT_WIDTH / 2 + 16, 10, str(state['p2_score']), 11)


def _render_p1(state):
  pyxel.rect(PLAYER_1_X, state['p1_y'], PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)


def _render_p2(state):
  pyxel.rect(PLAYER_2_X, state['p2_y'], PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)


def _render_ball(state):
  ball_x, ball_y = state['ball_xy']
  pyxel.rect(ball_x, ball_y, BALL_WIDTH, BALL_WIDTH, BALL_COLOR)

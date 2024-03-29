import pyxel

from match.constants import *
from label import ray_label, key_cap_label

def draw_from_state(state, is_primary):
  pyxel.rect(0, 0, COURT_WIDTH, COURT_HEIGHT, COURT_COLOR)
  print("is_primary", is_primary)
  phase = state['phase']
  if phase == 'starting':
    render_starting(state, is_primary)
  elif phase == 'playing':
    render_playing(state)
  elif phase == 'end':
    render_end(state)


def render_starting(state, is_primary):
  frame = state['frame']
  lan_match = state.get('lan_match', False)
  starting_label_text = 'Starting in' if frame < 30 else '3' if frame < 60 else '2' if frame < 90 else '1'
  starting_label = ray_label.RayLabel(starting_label_text, size=16.0, colors=(4, 5), origin=(COURT_WIDTH / 2, 90), alignment=ray_label.Alignment.CENTER)
  starting_label.draw()

  # P1 is always primary
  if lan_match:
    if is_primary:
      up_key_cap = key_cap_label.KeyCapLabel(key_str="Q", key_code=pyxel.KEY_Q, size=4.0, origin=(93, COURT_HEIGHT-30), alignment=ray_label.Alignment.LEFT)
      up_label = ray_label.RayLabel("Up", size=4.0, colors=(1, 1), origin=(93 + up_key_cap.width, COURT_HEIGHT-30), alignment=ray_label.Alignment.LEFT)
      down_key_cap = key_cap_label.KeyCapLabel(key_str="A", key_code=pyxel.KEY_A, size=4.0, origin=(133, COURT_HEIGHT-30), alignment=ray_label.Alignment.LEFT)
      down_label = ray_label.RayLabel("Down", size=4.0, colors=(1, 1), origin=(133 + down_key_cap.width, COURT_HEIGHT-30), alignment=ray_label.Alignment.LEFT)
      color_label = ray_label.RayLabel("You:", size=4.0, colors=(1, 1), origin=(104, COURT_HEIGHT-10), alignment=ray_label.Alignment.LEFT)
      color_text = ray_label.RayLabel("Yellow", size=4.0, colors=(6, 7), origin=(124, COURT_HEIGHT-10), alignment=ray_label.Alignment.LEFT)
    else:
      up_key_cap = key_cap_label.KeyCapLabel(key_str="O", key_code=pyxel.KEY_Q, size=4.0, origin=(93, COURT_HEIGHT-30), alignment=ray_label.Alignment.LEFT)
      up_label = ray_label.RayLabel("Up", size=4.0, colors=(1, 1), origin=(93 + up_key_cap.width, COURT_HEIGHT-30), alignment=ray_label.Alignment.LEFT)
      down_key_cap = key_cap_label.KeyCapLabel(key_str="L", key_code=pyxel.KEY_A, size=4.0, origin=(133, COURT_HEIGHT-30), alignment=ray_label.Alignment.LEFT)
      down_label = ray_label.RayLabel("Down", size=4.0, colors=(1, 1), origin=(133 + down_key_cap.width, COURT_HEIGHT-30), alignment=ray_label.Alignment.LEFT)
      color_label = ray_label.RayLabel("You:", size=4.0, colors=(1, 1), origin=(104, COURT_HEIGHT-10), alignment=ray_label.Alignment.LEFT)
      color_text = ray_label.RayLabel("Blue", size=4.0, colors=(12, 13), origin=(124, COURT_HEIGHT-10), alignment=ray_label.Alignment.LEFT)

    up_key_cap.draw()
    up_label.draw()
    down_key_cap.draw()
    down_label.draw()
    color_label.draw()
    color_text.draw()

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
  for i in range(-1, COURT_HEIGHT, 10):
    pyxel.rect((COURT_WIDTH / 2 - COURT_TICK_WIDTH / 2), i, COURT_TICK_WIDTH, COURT_TICK_HEIGHT, COURT_TICK_COLOR)


def _render_score(state):
  p1_score_text = str(state['p1_score']) if state['p1_score'] >= 10 else '0' + str(state['p1_score'])
  p2_score_text = str(state['p2_score']) if state['p2_score'] >= 10 else '0' + str(state['p2_score'])
  p1_score = ray_label.RayLabel(text=p1_score_text, typeface=ray_label.Typeface.ULTRAWIDE, size=12, colors=(6,7), origin=(0 + 20,COURT_HEIGHT - 5), alignment=ray_label.Alignment.CENTER)
  p2_score = ray_label.RayLabel(text=p2_score_text, typeface=ray_label.Typeface.ULTRAWIDE, size=12, colors=(12,13), origin=(COURT_WIDTH - 34,COURT_HEIGHT - 5), alignment=ray_label.Alignment.CENTER)
  p1_score.draw()
  p2_score.draw()


def _render_p1(state):
  pyxel.rectb(PLAYER_1_X, state['p1_y'], PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_1_COLOR)
  pyxel.line(PLAYER_1_X + PLAYER_WIDTH/2, state['p1_y']+2, PLAYER_1_X+PLAYER_WIDTH/2, state['p1_y']+PLAYER_HEIGHT-3, PLAYER_1_COLOR)

def _render_p2(state):
  pyxel.rectb(PLAYER_2_X, state['p2_y'], PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_2_COLOR)
  pyxel.line(PLAYER_2_X + PLAYER_WIDTH/2, state['p2_y']+2, PLAYER_2_X+PLAYER_WIDTH/2, state['p2_y']+PLAYER_HEIGHT-3, PLAYER_2_COLOR)


def _render_ball(state):
  ball_x, ball_y = state['ball_xy']
  # TODO: Decide whether to keep ball trail, could be fun for some bonus/secret mode
  # ball_trail = state['ball_trail']

  # if len(ball_trail) >= 2:
  #   ptx, pty = ball_trail[0]
  #   for tx, ty in ball_trail:
  #     pyxel.line(ptx, pty, tx, ty, BALL_TRAIL_COLOR)
  #     ptx = tx
  #     pty = ty

  pyxel.rect(ball_x, ball_y, BALL_WIDTH, BALL_WIDTH, BALL_COLOR)


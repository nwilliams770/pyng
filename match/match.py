"""
A 1-on-1 game instance

Should update or draw from state in ALL game cases?
  -- Always draw from state, regardless of game mode


"""

import pyxel
import random
import math

from match import match_type, engine, renderer
from match.constants import *


class Match():
  def __init__(self, match_type, multiplayer):
    self.state = None
    self.match_type = match_type

    self.should_close = False
    self.game_over = False

    self.multiplayer = multiplayer
    self.is_primary = multiplayer.is_primary

    if self.is_primary:
      self.engine = engine.Engine()

  def update(self):
    if self.is_primary:
      self.update_as_primary()
    else:
      self.update_as_secondary()

  def update_as_primary(self):
    p1_input, p2_input = self.get_inputs()
    self.state = self.engine.update(p1_input, p2_input)
    # self.multiplayer.send(state) TODO

  def update_as_secondary(self):
    # state = self.multiplayer.get_message() TODO
    # draw_from_state(state)
    # keys_pressed = TODO
    # self.multiplayer.send_message({'keys': keys_pressed})
    pass

  def draw(self):
    if not self.state:
      return

    renderer.draw_from_state(self.state)

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

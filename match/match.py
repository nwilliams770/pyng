"""
A 1-on-1 game instance
"""

# TODO
# - Test multiplayer

import pyxel
from enum import Enum

from library import multiplayer
from label import ray_label
from match import match_type, engine, renderer
import constants
from match.constants import *


class MatchPhase(Enum):
  STARTING = 1
  PLAYING = 2
  END = 3
  DISCONNECTED = 4

class Match():
  def __init__(self, match_type, multiplayer):
    self.state = None
    self.match_type = match_type
    self.winner = None
    self.game_over = False
    self.return_to_main_menu = False
    self.multiplayer = multiplayer
    self.is_primary = multiplayer.is_primary
    self.disconnected_header = ray_label.RayLabel(text='Disconnected', size=16.0, colors=(8,9), origin=(constants.GAME_WIDTH * .5, 80), alignment=ray_label.Alignment.CENTER)
    self.disconnected_message = ray_label.RayLabel(text='Returning to main menu', size=4.0, colors=(8,9), origin=(constants.GAME_WIDTH * .5, 100), alignment=ray_label.Alignment.CENTER)

    if self.is_primary:
      self.frame = 0
      self.match_phase = MatchPhase.STARTING
      self.engine = engine.Engine()
    self.multiplayer.start_new_game()

  def update(self):
    if self.is_primary:
      self.update_as_primary()
      self.frame += 1
    else:
      self.update_as_secondary()

  def send(self, msg):
    try:
      self.multiplayer.send(msg)
    except multiplayer.DisconnectError:
      if self.is_primary:
        self.match_phase = MatchPhase.DISCONNECTED
        self.frame = 0
      return False
    return True

  def update_as_primary(self):
    if self.match_phase == MatchPhase.DISCONNECTED:
      self.state = {'phase': 'disconnected'}
      if self.frame >= 45:
        self.return_to_main_menu = True
    else:
      if self.frame == 0:
        # On the first frame, we expect no inputs yet
        pass
      else:
        try:
          p1_input, p2_input = self.get_inputs()
        except multiplayer.DisconnectError:
          self.match_phase = MatchPhase.DISCONNECTED
          self.frame = 0
          return

      if self.match_phase == MatchPhase.STARTING:
        self.state = {'phase': 'starting', 'frame': self.frame}
        if isinstance(self.match_type, match_type.LANMultiplayer):
          self.state['lan_match'] = True
          ok = self.send(self.state)
          if not ok:
            return

        if self.frame >= 120:
          self.match_phase = MatchPhase.PLAYING
          print("Primary has just entered playing phase")
      elif self.match_phase == MatchPhase.PLAYING:
        # Reset if we've gotten inputs successfully
        self.state = self.engine.update(p1_input, p2_input)
        if isinstance(self.match_type, match_type.LANMultiplayer):
          ok = self.send(self.state)
          if not ok:
            return

        if winner := self.engine.check_for_winner():
          self.winner = winner
          self.match_phase = MatchPhase.END
          self.frame = 0 # reset the frame count to determine when to transition to rematch screen

      elif self.match_phase == MatchPhase.END:
        self.state['phase'] = 'end'
        self.state['frame'] = self.frame
        self.state['winner'] = self.winner
        if isinstance(self.match_type, match_type.LANMultiplayer):
          ok = self.send(self.state)
          if not ok:
            return
        if self.frame >= 60:
          self.game_over = True
      elif self.match_phase == MatchPhase.DISCONNECTED:
        pass

  def update_as_secondary(self):
    if self.state and self.state.get('phase') == 'disconnected':
      print("Seconday in disconnected state")
      # If we've disconnected, secondary manages its own frame count now
      self.frame += 1
      if self.frame >= 45:
        self.return_to_main_menu = True
      return

    try:
      self.state = self.multiplayer.check_for_received_message()
    except multiplayer.DisconnectError:
      self.state = { 'phase': 'disconnected' }
      self.frame = 0
      print("Seconday moved to disconnected state")
      return

    # Ack by sending back which keys are currently pressed
    if self.state.get('phase') == 'playing' or self.state.get('phase') == 'starting':
      _, p2_input = self.get_inputs()
      message = { 'key_pressed': p2_input }
    elif self.state['phase'] == 'end':
      # self.update_replay_menu()
      if self.state.get('frame') >= 60:
        self.game_over = True
      message = { 'key_pressed': None }

    if self.state.get('phase') != 'disconnected':
      ok = self.send(message)
      if not ok:
          print("Secondary wasn't able to send its inputs")
          # if we cannot send, we're disconnected :(
          self.state = { 'phase': 'disconnected' }
          self.frame = 0

  def draw(self):
    if not self.state:
      return

    renderer.draw_from_state(self.state, self.is_primary)

    if self.state['phase'] == 'disconnected':
      pyxel.cls(0)
      self.disconnected_header.draw()
      self.disconnected_message.draw()



# TODO: move to engine? only ever called by the primary
  def get_inputs(self):
    p1_input = None
    p2_input = None

    is_p1_local = True  # For now, even over LAN, p1 is always the primary
    is_p2_local = not isinstance(self.match_type, match_type.LANMultiplayer) or not self.multiplayer.is_primary

    if is_p1_local:
      if pyxel.btn(pyxel.KEY_Q) and pyxel.btn(pyxel.KEY_A):
        p1_input = None
      elif pyxel.btn(pyxel.KEY_Q):
        p1_input = pyxel.KEY_Q
      elif pyxel.btn(pyxel.KEY_A):
        p1_input = pyxel.KEY_A
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
      ack_message = self.multiplayer.check_for_received_message()
      p2_input = ack_message['key_pressed']

    return (p1_input, p2_input)

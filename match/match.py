"""
A 1-on-1 game instance

Should update or draw from state in ALL game cases?
  -- Always draw from state, regardless of game mode
"""

# TODO:
# - Replay: if match is end, primary needs to check for secondary
# - On replay opt, need to show message waiting for player input
# - On disconnect, show message to user, wait for 1-2s, then go back to main menu
#
# - Style board
# - Potentially look into collision detection? some weird behaviors sometimes
# - Coming soon on vs AI

import pyxel
import random
import math
from enum import Enum

from library import multiplayer
from match import match_type, engine, renderer, replay_menu
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
    # self.replay_menu = replay_menu.ReplayMenu()
    # self.return_to_menu = False
    # self.replay = False
    self.game_over = False

    self.multiplayer = multiplayer
    self.is_primary = multiplayer.is_primary

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

  # def update_replay_menu(self):
  #   self.replay_menu.update()

  #   if self.replay_menu.selection:
  #     if self.replay_menu.selection == "REMATCH":
  #       self.replay = True
  #     elif self.replay_menu.selection == "RETURN TO MENU":
  #       self.return_to_menu = True

  def send(self, msg):
    try:
      self.multiplayer.send(msg)
    except multiplayer.DisconnectError:
      if self.is_primary:
        self.match_phase = MatchPhase.DISCONNECTED
      return False

    return True

  def update_as_primary(self):
    if self.match_phase == MatchPhase.DISCONNECTED:
      self.state = {'phase': 'disconnected'}
    else:
      if self.frame == 0:
        # On the first frame, we expect no inputs yet
        pass
      else:
        try:
          p1_input, p2_input = self.get_inputs()
        except multiplayer.DisconnectError:
          self.match_phase = MatchPhase.DISCONNECTED
          return

      if self.match_phase == MatchPhase.STARTING:
        self.state = {'phase': 'starting', 'frame': self.frame}
        if isinstance(self.match_type, match_type.LANMultiplayer):
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
        # self.update_replay_menu()
        if self.frame >= 60:
          self.game_over = True
      elif self.match_phase == MatchPhase.DISCONNECTED:
        pass

  def update_as_secondary(self):
    if self.state and self.state.get('phase') == 'disconnected':
      print("Seconday in disconnected state")
      return

    try:
      self.state = self.multiplayer.check_for_received_message()
    except multiplayer.DisconnectError:
      # they dead
      self.state = { 'phase': 'disconnected' }
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

    ok = self.send(message)
    if not ok:
        print("Secondary wasn't able to send its inputs")
        # if we cannot send, we're disconnected :(
        self.state = { 'phase': 'disconnected' }

  def draw(self):
    if not self.state:
      return

    renderer.draw_from_state(self.state)

    # if self.state['phase'] == 'end':
      # self.replay_menu.draw()
    if self.state['phase'] == 'disconnected':
      # TODO - clean this up? have a new object? tbd
      import constants
      pyxel.rect(0, 0, constants.GAME_WIDTH, constants.GAME_HEIGHT, col=5)

# TODO: move to engine? only ever called by the primary
  def get_inputs(self):
    p1_input = None
    p2_input = None

    is_p1_local = True  # For now, even over LAN, p1 is always the primary
    is_p2_local = not isinstance(self.match_type, match_type.LANMultiplayer) or not self.multiplayer.is_primary
    # TODO is_p2_ai

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

"""
A 1-on-1 game instance

Should update or draw from state in ALL game cases?
  -- Always draw from state, regardless of game mode


"""

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
    self.replay_menu = replay_menu.ReplayMenu()
    self.return_to_menu = False
    self.replay = False

    self.multiplayer = multiplayer
    self.is_primary = multiplayer.is_primary

    if self.is_primary:
      self.frame = 0
      self.match_phase = MatchPhase.STARTING
      self.engine = engine.Engine()
      self.consecutive_dropped_responses = 0

  def update(self):
    if self.is_primary:
      self.frame += 1
      self.update_as_primary()
    else:
      self.update_as_secondary()

  def update_replay_menu(self):
    self.replay_menu.update()

    if self.replay_menu.selection:
      if self.replay_menu.selection == "REMATCH":
        self.replay = True
      elif self.replay_menu.selection == "RETURN TO MENU":
        self.return_to_menu = True

  def send(self, state):
    try:
      self.multiplayer.send(self.state)
    except multiplayer.DisconnectError:
      return False

    return True

  def update_as_primary(self):
    if self.match_phase == MatchPhase.STARTING:
      self.state = {'phase': 'starting', 'frame': self.frame}
      if self.multiplayer.is_connected:
        if not self.send(self.state):
          self.show_disconnected_as_primary()

      if self.frame >= 120:
        self.match_phase = MatchPhase.PLAYING

    if self.match_phase == MatchPhase.PLAYING:
      # If we're playing, get the inputs
      try:
        p1_input, p2_input = self.get_inputs()
      except multiplayer.NoMessageError:
        print(f"Did not hear inputs from Secondary, {self.consecutive_dropped_responses} in a row!")
        self.consecutive_dropped_responses += 1
        if self.consecutive_dropped_responses > 7:
          self.show_disconnected_as_primary()
        return

      # Reset if we've gotten inputs successfully
      self.consecutive_dropped_responses = 0
      self.state = self.engine.update(p1_input, p2_input)
      if self.multiplayer.is_connected:
        if not self.send(self.state):
          self.show_disconnected_as_primary()

      if winner := self.engine.check_for_winner():
        self.winner = winner
        self.match_phase = MatchPhase.END

    if self.match_phase == MatchPhase.END:
      self.state['phase'] = 'end'
      self.state['frame'] = self.frame
      self.state['winner'] = self.winner

      if self.multiplayer.is_connected:
        if not self.send(self.state):
          self.show_disconnected_as_primary()

      self.update_replay_menu()

    if self.match_phase == MatchPhase.DISCONNECTED:
      self.state['phase'] = 'disconnected'

  def show_disconnected_as_primary(self):
    self.match_phase = MatchPhase.DISCONNECTED

  def update_as_secondary(self):
    if self.state and self.state.get('phase') == 'disconnected':
      #TODO - update disconnect menu?
      return

    try:
      self.state = self.multiplayer.check_for_received_message()
    except multiplayer.DisconnectError:
      # we dead
      self.state = { 'phase': 'disconnected' }
      return

    if not self.state:
      # TODO error handling if state not received for x frames?
      print("Attempted update as secondary: did not receive any state")
      return

    # Ack by sending back which keys are currently pressed
    # Note: here is a good place to test dropped connections for error messaging
    #just replace below line with: if self.state['phase'] == 'playing'
    if self.state['phase'] == 'playing' or self.state['phase'] == 'starting':
      _, p2_input = self.get_inputs()
      message = {
        'key_pressed': p2_input
      }
      if not self.send(message):
        # if we cannot send, we're disconnected :(
        self.state = { 'phase': 'disconnected' }

    if self.state['phase'] == 'end':
      self.update_replay_menu()

  def draw(self):
    if not self.state:
      return

    renderer.draw_from_state(self.state)

    if self.state['phase'] == 'end':
      self.replay_menu.draw()
    elif self.state['phase'] == 'disconnected':
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
      if not ack_message or 'key_pressed' not in ack_message:
        raise multiplayer.NoMessageError()
      p2_input = ack_message['key_pressed']

    return (p1_input, p2_input)

"""
A menu screen for player(s) from a previous match
Can rematch or return to main menu
"""
import constants

from library import multiplayer
from label import ray_label
from menu.selection_menu import SelectionMenu
from match import match_type

class RematchMenu():
  def __init__(self, match_type, multiplayer):
    self.match_type = match_type
    self.multiplayer = multiplayer
    self.header = ray_label.RayLabel(text='Game Over', size=16.0, colors=(8,9), origin=(constants.GAME_WIDTH * .5, 20), alignment=ray_label.Alignment.CENTER)
    self.connecting_header = ray_label.RayLabel(text='Awaiting opponent...', size=4.0, colors=(4,5), origin=(constants.GAME_WIDTH * .5, 55), alignment=ray_label.Alignment.CENTER)
    self.opponent_found_header = ray_label.RayLabel(text='Opponent Found', size=4.0, colors=(4,5), origin=(constants.GAME_WIDTH * .5, 55), alignment=ray_label.Alignment.CENTER)
    self.disconnected_header = ray_label.RayLabel(text='Opponent disconnected', size=4.0, colors=(8,9), origin=(constants.GAME_WIDTH * .5, 55), alignment=ray_label.Alignment.CENTER)
    self.selection_menu = SelectionMenu(primary_options=['REMATCH', 'RETURN TO MAIN MENU'], option_padding=15)
    self.frame = 0
    self.return_to_main_menu = False
    self.multiplayer_disconnected = False
    self.restart_match = False
    self.state_transition_frame = 0

  @property
  def is_lan_match(self):
    return isinstance(self.match_type, match_type.LANMultiplayer)

  def handle_disconnect(self):
    self.multiplayer_disconnected = True
    self.state_transition_frame = self.frame

  def send(self, msg):
    try:
      self.multiplayer.send(msg)
    except multiplayer.DisconnectError:
      self.handle_disconnect()
      return False

    return True

  def update_for_lan_rematch(self):
    if self.multiplayer_disconnected:
      if self.frame - self.state_transition_frame >= 45:
        self.return_to_main_menu = True
      return
    elif self.selection_menu.selection == 'RETURN TO MAIN MENU':
      self.return_to_main_menu = True
    elif self.multiplayer.is_primary and self.frame == 0:
      return

    try:
      their_message = self.multiplayer.check_for_received_message()
    except multiplayer.DisconnectError:
      self.handle_disconnect()
      return

    message = {'rematch': (self.selection_menu.selection == 'REMATCH') }
    ok = self.send(message)
    if not ok:
      self.handle_disconnect()
      return

    if their_message.get('rematch') and message['rematch']:

      if self.state_transition_frame == 0:
        self.state_transition_frame = self.frame
      elif self.frame - self.state_transition_frame >= 45:
        self.restart_match = True
      return

  def update(self):
    self.selection_menu.update()

    if isinstance(self.match_type, match_type.LANMultiplayer):
      self.update_for_lan_rematch()
      self.frame += 1
    else:
      if self.selection_menu.selection == 'REMATCH':
        self.restart_match = True
      elif self.selection_menu.selection == 'RETURN TO MAIN MENU':
        self.return_to_main_menu = True

  def send(self, msg):
    try:
      self.multiplayer.send(msg)
    except multiplayer.DisconnectError:
      return False
    return True

  def draw(self):
    self.header.draw()
    self.selection_menu.draw()

    if self.is_lan_match:
      if self.selection_menu.selection == 'REMATCH' and not self.multiplayer_disconnected and self.state_transition_frame == 0:
        self.connecting_header.draw()
      elif self.selection_menu.selection == 'REMATCH' and not self.multiplayer_disconnected and self.state_transition_frame > 0:
        self.opponent_found_header.draw()
      elif self.multiplayer_disconnected:
        self.disconnected_header.draw()

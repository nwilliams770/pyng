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
    self.disconnected_header = ray_label.RayLabel(text='Opponent disconnected, returning to main menu...', size=4.0, colors=(8,9), origin=(constants.GAME_WIDTH * .5, 55), alignment=ray_label.Alignment.CENTER)
    self.selection_menu = SelectionMenu(primary_options=['REMATCH', 'RETURN TO MAIN MENU'], option_padding=15)
    self.frame = 0
    self.return_to_main_menu = False
    self.multiplyer_disconnected = False
    self.restart_match = False

  @property
  def is_lan_match(self):
    return isinstance(self.match_type, match_type.LANMultiplayer)

  def handle_disconnect(self):
    self.multiplayer_disconnected = True
    self.frame = 0

  def send(self, msg):
    try:
      self.multiplayer.send(msg)
    except multiplayer.DisconnectError:
      self.handle_disconnect()
      return False

    return True

  def update_for_lan_rematch(self):
    if self.multiplyer_disconnected:
      if self.frame >= 45:
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
      if self.selection_menu.selection == 'REMATCH' and not self.multiplyer_disconnected:
        self.connecting_header.draw()
      elif self.multiplyer_disconnected:
        self.disconnected_header.draw()

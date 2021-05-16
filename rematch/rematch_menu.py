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
    self.header = ray_label.RayLabel(text='Game Over', size=20.0, colors=(8,9), origin=(constants.GAME_WIDTH * .5, 20), alignment=ray_label.Alignment.CENTER)
    self.connecting_header = ray_label.RayLabel(text='Awaiting opponent...', size=20.0, colors=(4,5), origin=(constants.GAME_WIDTH * .5, 30), alignment=ray_label.Alignment.CENTER)
    self.disconnected_header = ray_label.RayLabel(text='Opponent disconnected, returning to main menu...', size=20.0, colors=(8,9), origin=(constants.GAME_WIDTH * .5, 30), alignment=ray_label.Alignment.CENTER)
    self.selection_menu = SelectionMenu(primary_options=['REMATCH', 'RETURN TO MAIN MENU'], option_padding=15)
    self.frame = 0
    self.return_to_main_menu = False
    self.multiplyer_disconnected = False
    self.restart_match = False

  @property
  def is_lan_match(self):
    return isinstance(self.match_type, match_type.LANMultiplayer)

  def send(self, msg):
    try:
      self.multiplayer.send(msg)
    except multiplayer.DisconnectError:
      self.multiplyer_disconnected = True
      self.frame = 0
      return False

    return True

  def update_as_primary(self):
    if self.multiplyer_disconnected:
      if self.frame >= 45:
        self.return_to_main_menu = True
      return
    elif self.frame == 0:
      return

    try:
      their_message = self.multiplayer.check_for_received_message()
    except multiplayer.DisconnectError:
      print("primary didn't get message, disconnected")
      self.multiplyer_disconnected = True
      self.frame = 0
      return

    message = {'rematch': (self.selection_menu.selection == 'REMATCH') }
    ok = self.send(message)
    if not ok:
      self.multiplyer_disconnected = True
      self.frame = 0
      return

    if their_message.get('rematch') and message['rematch']:
      self.restart_match = True

  def update_as_secondary(self):
    if self.multiplyer_disconnected:
      self.frame += 1
      if self.frame >= 45:
        self.return_to_main_menu = True
      return

    try:
      their_message = self.multiplayer.check_for_received_message()
    except multiplayer.DisconnectError:
      print("secondary didn't get message, disconnected")
      self.multiplyer_disconnected = True
      self.frame = 0
      return

    message = {'rematch': (self.selection_menu.selection == 'REMATCH') }
    ok = self.send(message)
    if not ok:
      print("secondary did not send message successfully")
      self.multiplyer_disconnected = True
      self.frame = 0
      return

    if their_message.get('rematch') and message['rematch']:
      self.restart_match = True

  def update(self):
    self.selection_menu.update()

    if isinstance(self.match_type, match_type.LANMultiplayer):
      if self.multiplayer.is_primary:
        self.update_as_primary()
      else:
        self.update_as_secondary()
      self.frame += 1
    else:
      if self.selection_menu.selection:
        if self.selection_menu.selection == 'REMATCH':
          pass
        elif self.selection_menu.selection == 'RETURN TO MAIN MENU':
          self.return_to_main_menu = True

  def send(self, msg):
    try:
      self.multiplayer.send(msg)
    except multiplayer.DisconnectError:
      self.multiplyer_disconnected = True
      return False
    return True

  def draw(self):
    self.header.draw()
    self.selection_menu.draw()

    if self.selection_menu.selection == 'REMATCH' and not self.multiplyer_disconnected:
      self.connecting_header.draw()
    elif self.multiplyer_disconnected:
      self.disconnected_header.draw()



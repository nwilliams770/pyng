"""
Starts as:

 < LOGO >
PRESS START

On any key:

 < LOGO >

Local Multi
LAN Multi
Local AI
Credits

"""
import random
import math
import pyxel

from .menu_state import MenuState
from .selection_menu import SelectionMenu
from .ai_menu import AIMenu
from .lan_connect_menu import LANConnectMenu
from .title_screen import TitleScreen
from .credits_screen import CreditsScreen
from .controls_screen import ControlsScreen
from match import match_type
import constants
from label import ray_label


class MainMenu():
  def __init__(self, multiplayer):
    self.i = 0
    self.multiplayer = multiplayer
    self.state = MenuState.TITLE_SCREEN

    # We'll set this to indicate we're ready to start a match
    self.match_type = None

    self.selection_menu = SelectionMenu(primary_options=['LOCAL MULTIPLAYER', 'ARTIFICIAL INTELLIGENCE', 'LAN CONNECT'], secondary_options=['CREDITS', 'CONTROLS'], option_padding=15, options_padding=20)
    self.ai_menu = AIMenu()
    self.lan_connection_menu = LANConnectMenu(multiplayer=multiplayer)
    self.title_screen = TitleScreen()
    self.credits_screen = CreditsScreen()
    self.controls_screen = ControlsScreen()


  def update(self):
    if self.state == MenuState.TITLE_SCREEN:
      self.title_screen.update()

      if self.title_screen.continue_to_selection:
        # do some transition here
        self.state = MenuState.SELECTION_MENU

    elif self.state == MenuState.SELECTION_MENU:
      self.selection_menu.update()

      if self.selection_menu.selection:
        if self.selection_menu.selection == 'LOCAL MULTIPLAYER':
          self.match_type = match_type.LocalMultiplayer()
        elif self.selection_menu.selection == 'ARTIFICIAL INTELLIGENCE':
          self.state = MenuState.AI_MENU
          # self.state = match_type.LocalAI()
        elif self.selection_menu.selection == 'LAN CONNECT':
          self.state = MenuState.LAN_CONNECT
        elif self.selection_menu.selection == 'CREDITS':
          self.state = MenuState.CREDITS
        elif self.selection_menu.selection == 'CONTROLS':
          self.state = MenuState.CONTROLS

        # Once we've taken the appropriate action based on user selection, reset
        # the selection for future times we'll land on this menu
        self.selection_menu.selection = None

    elif self.state == MenuState.AI_MENU:
      self.ai_menu.update()
      if self.ai_menu.navigate_to_menu:
        self.state = MenuState.SELECTION_MENU
        self.ai_menu.navigate_to_menu = False

    elif self.state == MenuState.LAN_CONNECT:
      self.lan_connection_menu.update()

      if self.lan_connection_menu.connected:
        self.match_type = match_type.LANMultiplayer()
        self.lan_connection_menu.connected = False
      elif self.lan_connection_menu.navigate_to_menu:
        self.state = MenuState.SELECTION_MENU
        self.lan_connection_menu.navigate_to_menu = False

    elif self.state == MenuState.CREDITS:
      self.credits_screen.update()

      if self.credits_screen.navigate_to_menu:
        self.state = MenuState.SELECTION_MENU
        self.credits_screen.navigate_to_menu = None

    elif self.state == MenuState.CONTROLS:
      self.controls_screen.update()

      if self.controls_screen.navigate_to_menu:
        self.state = MenuState.SELECTION_MENU
        self.controls_screen.navigate_to_menu = None

  def draw(self):
    pyxel.cls(0) # clear screen with black

    if self.state == MenuState.TITLE_SCREEN:
      self.title_screen.draw()

    elif self.state == MenuState.SELECTION_MENU:
      self.selection_menu.draw()

    elif self.state == MenuState.CREDITS:
      self.credits_screen.draw()

    elif self.state == MenuState.CONTROLS:
      self.controls_screen.draw()

    elif self.state == MenuState.LAN_CONNECT:
      self.lan_connection_menu.draw()

    elif self.state == MenuState.AI_MENU:
      self.ai_menu.draw()

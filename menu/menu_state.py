from enum import Enum

class MenuState(Enum):
  TITLE_SCREEN = 1
  SELECTION_MENU = 2
  AI_MENU = 3
  LAN_CONNECT = 4
  CREDITS = 5
  CONTROLS = 6

class LanConnectMenuState(Enum):
  COLLECTING_INPUT = 1
  CONNECTING = 2
  OPPONENT_FOUND = 3

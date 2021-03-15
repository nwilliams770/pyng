from enum import Enum

class MenuState(Enum):
  TITLE_SCREEN = 1
  SELECTION_MENU = 2
  LAN_CONNECT = 3
  CREDITS = 4
  CONTROLS = 5

class LanConnectMenuState(Enum):
  COLLECTING_INPUT = 1
  CONNECTING = 2
  OPPONENT_FOUND = 3

"""
Singleton application that manages top-level state and flow
For example, starts you in the menu, then when menu says "play game",
the app instantiates a match, ...
             ______________________________________
            V                                      |
* --> [ Main Menu ] <--> [ Play Match ] <--> [ Game Over ]
            A
            `---------> [ Credits ]

"""
import argparse
import time
import pyxel

from app_state import AppState
from library import multiplayer
from menu import main_menu
from match import match
import constants

PALETTE = [0x000000, 0xFFFFFF, 0x62FFFF, 0xBBFFFF, 0x71FF50, 0xB8FFA7, 0xFFE600, 0xFFF281, 0xD7160D, 0xFF3E35, 0xC31BFF, 0xCF49FF, 0x000A8D, 0x000DBC, 0x0, 0x0]

class App:
  def __init__(self, port):
    self.state = None

    self.main_menu = None
    self.match = None
    self.game_over = None
    self.credits = None

    self.multiplayer = multiplayer.Multiplayer(port=port)
    self.role = None
    pyxel.init(constants.GAME_WIDTH, constants.GAME_HEIGHT, scale=4, palette=PALETTE, fps=30, quit_key=pyxel.KEY_Q)
    pyxel.run(self.update, self.draw)

  # separate methods for each game state
  def update(self):
    # Check if we should change state
    if self.state is None:
      self.transition_to(state=AppState.MAIN_MENU, multiplayer=self.multiplayer)
    elif self.state == AppState.MAIN_MENU:
      if self.main_menu.match_type:
        self.transition_to(state=AppState.MATCH, match_type=self.main_menu.match_type, multiplayer=self.multiplayer)
    elif self.state == AppState.MATCH:
      pass
      # if self.match.should_close:
      #   self.transition_to(state=AppState.MAIN_MENU, multiplayer=self.multiplayer)
      # elif self.match.game_over:
      #   self.transition_to(state=AppState.GAME_OVER)
    elif self.state == AppState.GAME_OVER:
      if self.match.replay:
        pass # TODO: self.transition_to(state=AppState.MATCH, ...)
      elif self.match.should_close:
        self.transition_to(state=AppState.MAIN_MENU, multiplayer=self.multiplayer)
    elif self.state == AppState.CREDITS:
      if self.credits.should_close:
        self.transition_to(state=AppState.MAIN_MENU, multiplayer=self.multiplayer)

    # Now, update for the current state
    if self.state == AppState.MAIN_MENU:
      self.main_menu.update()
    elif self.state == AppState.MATCH:
      self.match.update()
    # elif ...

  def transition_to(self, state, **kwargs):
    assert(state != self.state)
    print(f"\t Transition to {state}")

    if state == AppState.MAIN_MENU:
      self.main_menu = main_menu.MainMenu(**kwargs)
    else:
      self.main_menu = None

    if state == AppState.MATCH:
      self.match = match.Match(**kwargs)

    self.state = state

  # separate methods for each game state
  def draw(self):
    pyxel.rect(x=0, y=0, w=constants.GAME_WIDTH, h=constants.GAME_HEIGHT, col=constants.COL_BG)

    if self.state == AppState.MAIN_MENU:
      self.main_menu.draw()
    elif self.state == AppState.MATCH:
      self.match.draw()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', type=int)
  args = parser.parse_args()
  App(port=args.port)

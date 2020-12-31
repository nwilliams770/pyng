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

import time
import pyxel

from app_state import AppState
from library import multiplayer
from menu import main_menu
from match import match


class App:
  def __init__(self):
    self.state = None

    self.main_menu = None
    self.match = None
    self.game_over = None
    self.credits = None

    self.server = multiplayer.MultiplayerServer(port=5555) # Todo: get port from enum or configuration, both players cant start on same port
    self.client = multiplayer.MultiplayerClient()
    self.role = None

    pyxel.init(140, 105, fps=30, quit_key=pyxel.KEY_Q)
    pyxel.run(self.update, self.draw)

  # separate methods for each game state
  def update(self):
    # Check if we should change state
    if self.state is None:
      self.transition_to(state=AppState.MAIN_MENU)
    elif self.state == AppState.MAIN_MENU:
      if self.main_menu.match_type:
        self.transition_to(state=AppState.MATCH, match_type=self.main_menu.match_type)
    elif self.state == AppState.MATCH:
      if self.match.should_close:
        self.transition_to(state=AppState.MAIN_MENU)
      elif self.match.game_over:
        self.transition_to(state=AppState.GAME_OVER)
    elif self.state == AppState.GAME_OVER:
      if self.match.replay:
        self.transition_to(state=AppState.MATCH)
      elif self.match.should_close:
        self.transition_to(state=AppState.MAIN_MENU)
    elif self.state == AppState.CREDITS:
      if self.credits.should_close:
        self.transition_to(state=AppState.MAIN_MENU)

    # Now, update for the current state
    if self.state == AppState.MAIN_MENU:
      self.main_menu.update()
    elif self.state == AppState.MATCH:
      self.match.update()
    # elif ...

  def transition_to(self, state, **kwargs):
    assert(state != self.state)

    if state == AppState.MAIN_MENU:
      self.main_menu = main_menu.MainMenu()
    else:
      self.main_menu = None

    if state == AppState.MATCH:
      self.match = match.Match(*kwargs)

    self.state = state

  # separate methods for each game state
  def draw(self):
    pyxel.rect(0, 0, 140, 105, 0)

    if self.state == AppState.MAIN_MENU:
      self.main_menu.draw()
    elif self.state == AppState.MATCH:
      self.match.draw()


if __name__ == '__main__':
  App()

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
import pyxel
from match import match_type

class MainMenu():
  def __init__(self, multiplayer):
    self.i = 0
    self.multiplayer = multiplayer

    # We'll set this to indicate we're ready to start a match
    self.match_type = None

    # TODO - refactor this into a better state tracker
    self.on_multiplayer_select_screen = True

  def update(self):
    self.i += 1

    if self.on_multiplayer_select_screen:
      # Whenever we're on the multiplayer screen, make sure we're running our server
      # so someone can connect to us.
      # Also, each frame, check if someone has connected.
      if not self.multiplayer.server.is_started:
        self.multiplayer.server.start()

      if self.multiplayer.server.check_for_connection():
        self.match_type = match_type.LANMultiplayer()
      elif pyxel.btnp(pyxel.KEY_ENTER):
        # Alternatively, a player can input their foe's address and initiate a connection
        # TODO - this is just the ENTEr key for now; make this on typing and submitting
        #        a valid host
        self.multiplayer.connect(host='127.0.0.1', port=5001 if self.multiplayer.port == 5002 else 5002)
        self.match_type = match_type.LANMultiplayer()

  def draw(self):
    pyxel.text(10, 10, s=f"{self.i}", col=3)



# self.input = ip_input.IpInput(screen_width=140, screen_height=105, bg_color=7, text_color=13) #Todo: pull these vals from config

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
  def __init__(self):
    self.i = 0
    pass

  def update(self):
    self.i += 1

    if pyxel.btnp(pyxel.KEY_ENTER):
      self.match_type = match_type.LocalMultiplayer()
    else:
      self.match_type = None

  def draw(self):
    pyxel.text(10, 10, s=f"{self.i}", col=3)



# self.input = ip_input.IpInput(screen_width=140, screen_height=105, bg_color=7, text_color=13) #Todo: pull these vals from config



  # def update_select_opponent(self):
  #   if not self.server.is_started:
  #     print("\t Starting server")
  #     self.server.start()
  #   elif self.server.is_connected:
  #     print("\t Server: connected!")
  #     self.state = AppState.GAME_INTRO

  #   self.input.update()

  #   if self.input.input_submitted:
  #     print("\t User typed in their opponent's IP")
  #     host = self.input.value
  #     self.client.connect(host=host, port=self.server.port)
  #     self.server.check_for_connection()
  #     print("\t Client: connected! Shutting down our server")
  # def draw_select_opponent_scene(self):


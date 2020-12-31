import multiplayer
import time
import pyxel
import ip_input


MODE_SELECT_OPPONENT = 'Select Opponent'
MODE_GAME_INTRO = 'Game Intro'
MODE_PLAYING_GAME = 'Playing Game'
MODE_GAME_END = 'Game End'

ROLE_PRIMARY = 'primary'
ROLE_SECONDARY = 'secondary'



# class App:
#   def __init__(self):
#     self.frame = 0
#     self.mode = MODE_SELECT_OPPONENT
#     self.server = multiplayer.MultiplayerServer(port=5555)
#     self.client = multiplayer.MultiplayerClient()
#     self.input = ip_input.IpInput(screen_width=140, screen_height=105, bg_color=7, text_color=13)
#     self.role = None
#     pyxel.init(140, 105, fps=30, quit_key=pyxel.KEY_Q)
#     pyxel.run(self.update, self.draw)

#   def draw(self):
#     if self.mode == MODE_SELECT_OPPONENT:
#       self.draw_select_opponent_scene()

#   def draw_select_opponent_scene(self):
#     pyxel.rect(0,0,140,105, 12)
#     self.input.draw()

#   def update(self):
#     self.frame += 1
#     # print("Frame {}: \t{}".format(self.frame, self.mode))

#     if self.mode == MODE_SELECT_OPPONENT:
#       if not self.server.is_started:
#         print("\t Starting server")
#         self.server.start()
#       elif self.server.is_connected:
#         print("\t Server: connected!")
#         self.mode = MODE_GAME_INTRO

#       self.input.update()


#       if self.input.input_submitted:
#         print("\t User typed in their opponent's IP")
#         host = self.input.value
#         self.client.connect(host=host, port=self.server.port)
#         self.server.check_for_connection()
#         print("\t Client: connected! Shutting down our server")
#     elif self.mode == MODE_GAME_INTRO:
#       self.mode = MODE_PLAYING_GAME
#     elif self.mode == MODE_PLAYING_GAME:
#       self.update_game()

#   def update_game(self):
#     pass  # TODO

# def run_as_primary():
#   print("I'm running as the Primary!")

# def run_as_replica():
#   print("I'm running as the Replica!")


def main():
  PLAYER_A_PORT = 5005
  PLAYER_B_PORT = 5006

  player_a_server = multiplayer.MultiplayerServer(port=PLAYER_A_PORT)
  player_b_server = multiplayer.MultiplayerServer(port=PLAYER_B_PORT)

  player_a_server.start()
  player_b_server.start()

  print("both started!")

  assert(player_a_server.is_connected is False)
  assert(player_a_server.check_for_connection() is False)

  # Simulate Player A connecting to Player B
  # Player A types this in:
  player_a_input_host = '127.0.0.1'
  player_a_input_port = PLAYER_B_PORT

  # That triggers the client to connect to the typed-in host/port
  player_a_client = multiplayer.MultiplayerClient()
  player_a_client.connect(host=player_a_input_host, port=player_a_input_port)
  print("Player A connected to Player B!")

  assert(player_b_server.check_for_connection() is True)
  assert(player_b_server.is_connected is True)
  print("...and Player B sees that it has a client!")

  # Simulate game start
  message = {'action': 'start_game'}
  player_b_server.send(message)
  print("Player B sent 'Start Game'")
  message = player_a_client.check_for_received_message()
  assert(message is not None)
  print("...and Player A received it! {}".format(message))

  # Have Player A confirm all-good
  message = {'hello': 'world'}
  player_a_client.send(message)
  print("Player A sent ack")
  message = player_b_server.check_for_received_message()
  print("...and Player B received ack: {}".format(message))

if __name__ == '__main__':
  # app = App()
  main()


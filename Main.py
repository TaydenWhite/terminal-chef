from pynput.keyboard import Key, Listener
from Game import Game



def send_inputs(key, game):
    if key == Key.esc: return False
    game.state_control(str(key))

def play_game():
    game = Game() # could have parameters to change 

    with Listener(on_press = lambda key: send_inputs(key, game)) as listener:
        listener.join()

play_game()
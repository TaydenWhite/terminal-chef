from pynput.keyboard import Key, Listener
from Game import Game
import Room
import Customer




def send_inputs(key, game):

    if key == Key.esc: 
        return False
    
    game.state_control(str(key))
    
 

def play_game():

    game = Game()

    with Listener(on_press = lambda key: send_inputs(key, game)) as listener:
        listener.join()

play_game()
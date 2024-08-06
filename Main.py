from pynput.keyboard import Key, Listener
from Game import Game
import Room
import Customer


game = Game()


def game_events(key):
   
    movements = [Key.up, Key.down, Key.left, Key.right]

    if key in movements:
        game.move(str(key))
        print(game.curr_room)


    strkey = str(key)

    print(strkey)

    if key == Key.esc: 
        return False
 
# Collect all event until released
with Listener(on_press = game_events) as listener:
    listener.join()
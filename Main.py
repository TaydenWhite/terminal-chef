from pynput.keyboard import Key, Listener
import Game
from Room import Pantry
import Item
import Ingredient
from Customer import Customer
from datetime import datetime, timedelta
import time


def send_inputs(key, game):

    if key == Key.up:
        current_time = datetime.now()
        end_time = (current_time + timedelta(seconds=10)).time()
        game.set_end_time = end_time
        print(f"Setting an END time to: {end_time}")
        


    if key == Key.esc: 
        return False
    
    game.state_control(str(key))
    
 

def play_game():

    # create game
    pantry = Pantry()


    customers = [Customer(Item(['Bread', 'Beef'], [], ['Potato'], 0, 'order'), 13), # Burger & Fries
                 Customer(Item(['Bread', 'Beef'], ['Lettuce', 'Tomato'], [], 0, 'order'), 10), # Burger w/ Lettuce, Tomato
                 Customer(Item(['Tomato'], [], ['Lettuce'], 0, 'order'), 8)] # Tomato Soup & Salad
    game = Game()



    with Listener(on_press = lambda key: send_inputs(key, game)) as listener:
        now = datetime.now().time()
        if now >= game.end_time:  # Use >= to ensure you catch the time even if a bit late
            print(f"It's time! Current time is: {now}")
        listener.join()

play_game()
from pynput.keyboard import Key, Listener
from datetime import datetime, timedelta
import time

end_time = (datetime.now() + timedelta(seconds=60)).time()

def send_inputs(key):

    if key == Key.up:
        current_time = datetime.now()
        global end_time 
        end_time = (current_time + timedelta(seconds=10)).time()
        print(f"Setting an END time to: {end_time}")  

    if key == Key.esc: 
        return False

def play_game():

    with Listener(on_press = send_inputs) as listener:
        now = datetime.now().time()
        global end_time
        if now >= end_time:  # Use >= to ensure you catch the time even if a bit late
            print(f"It's time! Current time is: {now}")
        listener.join()

play_game()
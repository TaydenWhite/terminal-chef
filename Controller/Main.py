from pynput.keyboard import Key, Listener
from Game_Runner import Game_Runner

def send_inputs(key, runner):
    if key == Key.esc: return False
    runner.state_control(str(key))

def play_game():
    runner = Game_Runner()

    listener = Listener(on_press=lambda key: send_inputs(key, runner))
    listener.start()

    try:
        while True:
            if not listener.running: break
    except KeyboardInterrupt: listener.stop()  

play_game()
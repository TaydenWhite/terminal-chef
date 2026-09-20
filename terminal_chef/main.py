"""Entry point: main menu loop."""

from .food import DISH_NAMES
from .game import ConsoleIO, Game, recipes_box

MAIN_MENU = r'''   //============================\\
   ||  WELCOME TO TERMINAL CHEF  ||
   ||                   __       ||
   ||       ^~^~^~^    (  )      ||
   ||      (       )    ||       ||
   ||       |_!_!_|     ||       ||
   ||       ' ' ' '     ()       ||
   ||                            ||
   ||  CREATED BY: TAYDEN WHITE  ||
   \\============================//
      ||   1) START A GAME    ||
      ||   2) TUTORIAL        ||
      ||   3) VIEW RECIPES    ||
      ||   4) FASTEST GAMES   ||
      \\======================//'''

PERMISSION_HELP = '''Terminal Chef could not read the keyboard.
On macOS, allow your terminal app under System Settings > Privacy & Security >
Input Monitoring (and Accessibility), then run the game again.'''


def run_game(keyboard, io):
    """Play one game. ESC pauses; failing the pause question ends the run."""
    game = Game(io)
    game.start()
    while not game.over:
        event = keyboard.get(0.1)
        if event is None:
            continue
        kind, key = event
        if kind == 'press':
            game.press(key)
        else:
            game.release(key)


def main():
    from .keyboard import Keyboard
    try:
        keyboard = Keyboard()
    except Exception:
        print(PERMISSION_HELP)
        return 1
    io = ConsoleIO()
    try:
        io.raw('\033[2J\033[H')  # clear the screen at launch
        io.line(MAIN_MENU)
        io.line('')
        while True:
            event = keyboard.get(0.1)
            if event is None or event[0] != 'press':
                continue
            key = event[1]
            if key == 'ESC':
                break
            if key == '1':
                run_game(keyboard, io)
            elif key == '3':
                io.line(recipes_box(DISH_NAMES).render())
                io.line('')
            else:
                continue  # TUTORIAL and FASTEST GAMES are not built yet
            io.line(MAIN_MENU)
            io.line('')
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.close()
    return 0

"""Entry point: main menu loop."""

from .food import DISH_NAMES
from .game import ConsoleIO, Game, fastest_box, recipes_box, tutorial_box

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
      ||   1) SHORT GAME      ||
      ||   2) LONG GAME       ||
      ||   3) TUTORIAL        ||
      ||   4) VIEW RECIPES    ||
      ||   5) FASTEST GAMES   ||
      ||   6) EXIT            ||
      \\======================//'''

NO_TERMINAL_HELP = '''Terminal Chef needs an interactive terminal.
Run it in a terminal window rather than through a pipe, or from an editor
console that does not forward keystrokes.'''

SHORT_GAME = {'mode': 'short', 'orders': 6, 'distinct': 6}
LONG_GAME = {'mode': 'long', 'orders': 12, 'distinct': 8}


def run_game(keyboard, io, mode, orders, distinct):
    """Play one game. ESC pauses; failing the pause question ends the run."""
    game = Game(io, mode=mode, orders=orders, distinct=distinct)
    game.start()
    while not game.over:
        key = keyboard.get(0.1)
        if key is not None:
            game.press(key)


def main():
    from .keyboard import NoTerminal, open_keyboard
    try:
        keyboard = open_keyboard()
    except NoTerminal:
        print(NO_TERMINAL_HELP)
        return 1
    io = ConsoleIO()
    try:
        io.raw('\033[2J\033[H')  # clear the screen at launch
        io.line(MAIN_MENU)
        io.line('')
        while True:
            key = keyboard.get(0.1)
            if key is None:
                continue
            if key in ('ESC', '6'):
                break
            if key == '1':
                run_game(keyboard, io, **SHORT_GAME)
            elif key == '2':
                run_game(keyboard, io, **LONG_GAME)
            elif key == '3':
                io.line(tutorial_box().render())
                io.line('')
            elif key == '4':
                io.line(recipes_box(DISH_NAMES).render())
                io.line('')
            elif key == '5':
                io.line(fastest_box().render())
                io.line('')
            else:
                continue
            io.line(MAIN_MENU)
            io.line('')
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.close()
    return 0

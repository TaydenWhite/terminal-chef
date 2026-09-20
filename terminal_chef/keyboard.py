"""Single-keypress input with no third-party dependencies.

Reads keys straight from the terminal: `termios` on macOS and Linux, `msvcrt`
on Windows. Recognised keys are UP DOWN LEFT RIGHT (arrows or WASD), E, R, ESC,
ENTER, BACKSPACE and the digits; anything else reads as None and is ignored.

Only presses are reported. There is no way to detect a key being released
without a desktop-wide hook, which is why the E and R peek menus toggle.
"""

import os
import sys
import time

LETTERS = {'w': 'UP', 's': 'DOWN', 'a': 'LEFT', 'd': 'RIGHT', 'e': 'E', 'r': 'R'}
POSIX_ARROWS = {'A': 'UP', 'B': 'DOWN', 'C': 'RIGHT', 'D': 'LEFT'}
WINDOWS_ARROWS = {'H': 'UP', 'P': 'DOWN', 'M': 'RIGHT', 'K': 'LEFT'}


class NoTerminal(Exception):
    """Raised when stdin is not an interactive terminal."""


def key_name(char):
    if char in ('\r', '\n'):
        return 'ENTER'
    if char in ('\x7f', '\x08'):
        return 'BACKSPACE'
    if char.isdigit():
        return char
    return LETTERS.get(char.lower())


class PosixKeyboard:
    def __init__(self):
        import termios
        import tty
        if not sys.stdin.isatty():
            raise NoTerminal
        self._termios = termios
        self._fd = sys.stdin.fileno()
        self._saved = termios.tcgetattr(self._fd)
        tty.setcbreak(self._fd)  # no echo, no line buffering

    def _read(self, timeout):
        import select
        ready, _, _ = select.select([self._fd], [], [], timeout)
        if not ready:
            return None
        # Read the descriptor directly: sys.stdin would buffer the rest of an
        # arrow-key sequence where select cannot see it, turning arrows into ESC.
        data = os.read(self._fd, 1)
        return data.decode('latin-1') if data else None

    def get(self, timeout=0.1):
        char = self._read(timeout)
        if char is None:
            return None
        if char != '\x1b':
            return key_name(char)
        # Either ESC on its own, or the start of an arrow sequence like ESC [ A.
        following = self._read(0.05)
        if following is None:
            return 'ESC'
        if following == '[':
            return POSIX_ARROWS.get(self._read(0.05) or '')
        return None

    def close(self):
        import select
        # Swallow anything still sitting in the input buffer, then restore the
        # old mode with TCSAFLUSH, which discards input as part of the same
        # operation. Restoring first would re-enable echo while keystrokes were
        # still queued, handing them to the shell to print back and beep at.
        try:
            while select.select([self._fd], [], [], 0)[0]:
                if not os.read(self._fd, 4096):
                    break
        except OSError:
            pass
        self._termios.tcsetattr(self._fd, self._termios.TCSAFLUSH, self._saved)


class WindowsKeyboard:
    def __init__(self):
        import msvcrt
        if not sys.stdin.isatty():
            raise NoTerminal
        self._msvcrt = msvcrt
        self._enable_ansi()

    @staticmethod
    def _enable_ansi():
        """Let the console act on the escape code the game uses to clear itself."""
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)

    def get(self, timeout=0.1):
        deadline = time.monotonic() + timeout
        while True:
            if self._msvcrt.kbhit():
                char = self._msvcrt.getwch()
                if char in ('\x00', '\xe0'):  # prefix for arrows and function keys
                    return WINDOWS_ARROWS.get(self._msvcrt.getwch())
                if char == '\x1b':
                    return 'ESC'
                return key_name(char)
            if time.monotonic() >= deadline:
                return None
            time.sleep(0.01)

    def close(self):
        pass


def open_keyboard():
    return WindowsKeyboard() if sys.platform == 'win32' else PosixKeyboard()

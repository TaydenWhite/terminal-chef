"""Keyboard input via pynput, with terminal echo switched off while the game runs.

Events are queued as ('press', KEY) / ('release', KEY) where KEY is one of
UP DOWN LEFT RIGHT (arrows or WASD), E, R, ESC, ENTER, BACKSPACE, or a digit."""

import queue
import sys
import termios
import time
import tty

LETTERS = {'w': 'UP', 's': 'DOWN', 'a': 'LEFT', 'd': 'RIGHT', 'e': 'E', 'r': 'R'}


class Keyboard:
    def __init__(self):
        self.events = queue.Queue()
        self._fd = self._saved = None
        if sys.stdin.isatty():
            self._fd = sys.stdin.fileno()
            self._saved = termios.tcgetattr(self._fd)
            tty.setcbreak(self._fd)  # no echo, no line buffering
        from pynput import keyboard as pk
        self._special = {pk.Key.up: 'UP', pk.Key.down: 'DOWN', pk.Key.left: 'LEFT', pk.Key.right: 'RIGHT',
                         pk.Key.esc: 'ESC', pk.Key.enter: 'ENTER', pk.Key.backspace: 'BACKSPACE'}
        self._key_type = pk.Key
        self._listener = pk.Listener(on_press=self._on_press, on_release=self._on_release)
        self._listener.daemon = True
        self._listener.start()
        time.sleep(0.3)
        if not self._listener.running:
            self.close()
            raise RuntimeError('keyboard listener failed to start')

    def _normalize(self, key):
        if isinstance(key, self._key_type):
            return self._special.get(key)
        char = getattr(key, 'char', None)
        if not char:
            return None
        char = char.lower()
        if char.isdigit():
            return char
        return LETTERS.get(char)

    def _on_press(self, key):
        name = self._normalize(key)
        if name:
            self.events.put(('press', name))

    def _on_release(self, key):
        name = self._normalize(key)
        if name:
            self.events.put(('release', name))

    def get(self, timeout=0.1):
        try:
            return self.events.get(timeout=timeout)
        except queue.Empty:
            return None

    def close(self):
        self._listener.stop()
        if self._fd is not None:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._saved)
            termios.tcflush(self._fd, termios.TCIFLUSH)  # drop keys typed during the game

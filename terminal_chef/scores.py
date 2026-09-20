"""Fastest finished games, kept in the player's home directory.

Stored in the home directory rather than beside the package so the file
survives reinstalls and stays writable when the game is installed with pipx.
Every read and write tolerates a missing, unreadable or corrupt file: losing
high scores must never stop someone playing.
"""

import json
from pathlib import Path

PATH = Path.home() / '.terminal-chef' / 'scores.json'
MODES = ('short', 'long')
KEEP = 10  # how many times to remember per mode


def load():
    """{'short': [seconds, ...], 'long': [...]}, fastest first."""
    try:
        data = json.loads(PATH.read_text())
    except (OSError, ValueError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    result = {}
    for mode in MODES:
        times = data.get(mode)
        clean = [t for t in times if isinstance(t, (int, float)) and t > 0] if isinstance(times, list) else []
        result[mode] = sorted(clean)[:KEEP]
    return result


def record(mode, seconds):
    """Add a finished game's time and keep only the fastest few."""
    data = load()
    if mode not in data:
        return data
    data[mode] = sorted(data[mode] + [round(seconds, 1)])[:KEEP]
    try:
        PATH.parent.mkdir(parents=True, exist_ok=True)
        PATH.write_text(json.dumps(data))
    except OSError:
        pass  # a read-only home directory should not break the game
    return data

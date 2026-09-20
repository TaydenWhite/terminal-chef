# Terminal Chef

A low-graphics cooking game that lives entirely in your terminal. You run a
kitchen out of seven rooms, cooking and plating what three customers order
while the trash piles up behind you.

No dependencies beyond Python itself. Works on macOS, Linux and Windows.

## Install

```
pipx install git+https://github.com/TaydenWhite/terminal-chef
terminal-chef
```

Or run it straight from a clone:

```
git clone https://github.com/TaydenWhite/terminal-chef
cd terminal-chef
python3 chef.py
```

It needs a real terminal window. Running it through a pipe, or from an editor
console that does not forward keystrokes, will not work.

## Controls

| Key | Does |
| --- | --- |
| Arrow keys or WASD | Move between rooms |
| 1 to 4 | Menu selections |
| E | Show EVERYTHING: orders, inventory, counters and running processes |
| R | Show RECIPES for the orders on the board right now |
| ESC | Pause |

Movement only works from an `ENTERED: ROOM` screen. E and R toggle: press
either to open it, then any other key closes it and reprints where you were.

Pausing freezes every timer behind a single multiplication question. Get it
right and play resumes exactly where it stopped. Get it wrong and the run ends.

## The kitchen

```
[SERVICE]
[PLATING] [STOVES]    [PANTRY]
[COUNTERS][PREP ROOM] [CLEANING]
```

- **Service** is where customers order, eat, and leave you a dirty plate.
- **Plating** holds three plates. You stack finished ingredients onto them here.
- **Stoves** has two pans and a pot.
- **Pantry** has the fridge and the shelf, with unlimited ingredients.
- **Counters** park three items, but anything with food on it expires.
- **Prep room** has the cutting board and the sink.
- **Cleaning** has the dish washer, the trash disposal and the discard bin.

## Making a dish

1. Take ingredients from the pantry.
2. Process them until they read `[RTP]`, ready to plate.
3. Stack them onto a plate in the plating room, in recipe order.
4. Carry the plate to the customer who ordered it.
5. Take the dirty plate back and run it through the dish washer.

Every ingredient has its own path, and the steps must happen in this order:

| Ingredient | Steps |
| --- | --- |
| Beef | Cook, then cut |
| Chicken | Wash, cook, then cut |
| Lettuce | Wash, then cut |
| Tomato | Wash, cut, then cook |
| Potato | Cut, then cook |
| Bread | Cut |

Stopping early matters. A cooked but uncut piece of beef is a burger patty; cut
it as well and it becomes a steak. The game refuses anything that is not a legal
next step for some recipe, and says nothing when it does, so check your tags.

## Trash

Trash runs from 0 to 10 and is the main thing working against you. Every
finished process adds some: pans, pots, the cutting board, the sink and the dish
washer each add 1, burning food adds 2 on top of the 1 for finishing cooking,
and anything left to expire on a counter adds 3.

From level 8 up, everything you start runs slower: 5 extra seconds at 8, 10 at 9
and 15 at 10. Clear it in the cleaning room, where the trash disposal resets it
to zero once you answer three multiplication questions and wait out the cycle.

## Watch out

- Food left in a pan or pot after it finishes cooking starts burning, and is
  gone for good 30 seconds later.
- A clean, empty plate never expires on a counter, but a plate with food does,
  and it comes back dirty.
- There are only three plates. Wash them.

## Game lengths

A short game is 6 customers, a long game is 12. Finishing either records your
time, and the fastest ten of each are listed under FASTEST GAMES. Times are kept
in `~/.terminal-chef/scores.json`. Quitting through a failed pause records
nothing.

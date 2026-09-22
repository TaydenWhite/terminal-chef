"""Timed stations: pans, pot, cutting board, sink, dish washer, disposal,
counters, and customers. Each station exposes `timer` (None when idle) and
`fire(game)`, which the game calls when the timer runs out."""

import math

from .food import Ingredient, Plate

BURN_SECONDS = 30
EAT_SECONDS = 30
WASHER_SECONDS = 30
DISPOSAL_SECONDS = 15
EXPIRE_SECONDS = 30
CUT_SECONDS = 10
WASH_SECONDS = 5
PENALTY = {8: 5, 9: 10, 10: 15}  # extra seconds by trash level at start


def penalty(trash):
    return PENALTY.get(trash, 0)


def plural(n, word):
    return f'{n} {word}' + ('' if n == 1 else 'S')


class Timer:
    def __init__(self, start, seconds):
        self.start = start
        self.end = start + seconds

    def remaining(self, now):
        return max(0, math.ceil(self.end - now))


class Cooker:
    """A pan or the pot. Cooking rolls straight into burning, then the food is gone."""

    def __init__(self, kind, label):
        self.kind = kind
        self.label = label
        self.item = None
        self.phase = None  # None, 'COOKING', 'BURNING'
        self.timer = None

    @property
    def selectable(self):
        return self.phase != 'COOKING'

    def accepts(self, ingredient):
        return (self.item is None and ingredient.next_step == 'COOK'
                and ingredient.vessel == self.kind)

    def start(self, ingredient, now, trash):
        self.item = ingredient
        self.phase = 'COOKING'
        self.timer = Timer(now, ingredient.cook_seconds + penalty(trash))

    def fire(self, game):
        if self.phase == 'COOKING':
            self.item.advance()
            game.add_trash(1)
            self.phase = 'BURNING'
            self.timer = Timer(self.timer.end, BURN_SECONDS)
        else:
            self.item, self.phase, self.timer = None, None, None
            game.add_trash(2)

    def can_take(self):
        return self.phase == 'BURNING'

    def take(self):
        item = self.item
        self.item, self.phase, self.timer = None, None, None
        return item

    def head(self, now):
        """(content, right value) for the ENTERED: STOVES status lines."""
        if self.phase is None:
            return 'EMPTY', None
        marker = 'C' if self.phase == 'COOKING' else 'B'
        return self.item.name, f'{self.timer.remaining(now)} SEC [{marker}]'

    def time_text(self, now):
        return self.head(now)[1]

    def process_name(self):
        name = f'{self.label} [{self.item.name}]'
        return name + ' [B]' if self.phase == 'BURNING' else name


class Prepper:
    """The cutting board or the sink. Runs once, then holds the finished item."""

    def __init__(self, step, label, seconds, short):
        self.step = step
        self.label = label
        self.short = short  # name used on the ENTERED: PREP ROOM status lines
        self.seconds = seconds
        self.item = None
        self.phase = None  # None, 'RUNNING', 'COMPLETE'
        self.timer = None

    @property
    def selectable(self):
        return self.phase != 'RUNNING'

    def accepts(self, ingredient):
        return self.item is None and ingredient.next_step == self.step

    def start(self, ingredient, now, trash):
        self.item = ingredient
        self.phase = 'RUNNING'
        self.timer = Timer(now, self.seconds + penalty(trash))

    def fire(self, game):
        self.item.advance()
        game.add_trash(1)
        self.phase = 'COMPLETE'
        self.timer = None

    def can_take(self):
        return self.phase == 'COMPLETE'

    def take(self):
        item = self.item
        self.item, self.phase, self.timer = None, None, None
        return item

    def head(self, now):
        """(content, right value) for the ENTERED: PREP ROOM status lines."""
        if self.phase is None:
            return 'EMPTY', None
        if self.phase == 'RUNNING':
            return self.item.name, f'{self.timer.remaining(now)} SEC'
        return self.item.name, 'COMPLETE'

    def time_text(self, now):
        return None

    def process_name(self):
        return f'{self.label} [{self.item.name}]'


class DishWasher:
    CAPACITY = 3
    label = 'DISH WASHER'

    def __init__(self):
        self.plates = []
        self.timer = None

    @property
    def running(self):
        return self.timer is not None

    def can_add(self):
        return not self.running and len(self.plates) < self.CAPACITY

    def add(self, plate):
        if plate.items:
            plate.soil()
        self.plates.append(plate)

    def start(self, now, trash):
        if self.running or not self.plates:
            return False
        self.timer = Timer(now, WASHER_SECONDS + penalty(trash))
        return True

    def fire(self, game):
        for plate in self.plates:
            plate.dirty = False
        self.timer = None
        game.add_trash(1)

    def clean_plates(self):
        return [p for p in self.plates if not p.dirty]

    def retrieve(self):
        plate = self.clean_plates()[0]
        self.plates.remove(plate)
        return plate

    def _counts(self):
        dirty = sum(1 for p in self.plates if p.dirty)
        return dirty, len(self.plates) - dirty

    def status_short(self, now):
        if self.running:
            return f'{self.timer.remaining(now)} SEC'
        if not self.plates:
            return 'EMPTY'
        dirty, clean = self._counts()
        return f'{dirty} DIRTY' if dirty else f'{clean} CLEAN'

    def status_long(self, now):
        if self.running:
            return f'{self.timer.remaining(now)} SEC'
        if not self.plates:
            return 'EMPTY'
        dirty, clean = self._counts()
        return plural(dirty, 'DIRTY PLATE') if dirty else plural(clean, 'CLEAN PLATE')

    def process_name(self):
        return self.label


class Disposal:
    label = 'TRASH DISPOSAL'

    def __init__(self):
        self.timer = None

    @property
    def running(self):
        return self.timer is not None

    def start(self, now, trash):
        # Deliberately exempt from the trash-level penalty: the one process
        # that clears trash must not be slowed down by it.
        self.timer = Timer(now, DISPOSAL_SECONDS)

    def fire(self, game):
        # Zeroed outright, so anything added while the cycle ran goes too.
        game.trash = 0
        self.timer = None

    def status(self, now):
        return f'{self.timer.remaining(now)} SEC' if self.running else 'EMPTY'

    def process_name(self):
        return self.label


class Counter:
    """Holds one item. Ingredients and plated food expire after 30 seconds;
    empty plates, clean or dirty, never do."""

    def __init__(self, label):
        self.label = label
        self.item = None
        self.timer = None

    def store(self, item, now):
        self.item = item
        expirable = isinstance(item, Ingredient) or bool(item.items)
        self.timer = Timer(now, EXPIRE_SECONDS) if expirable else None

    def fire(self, game):
        if isinstance(self.item, Plate):
            self.item.soil()
        else:
            self.item = None
        self.timer = None
        game.add_trash(3)

    def can_take(self):
        return self.item is not None

    def take(self):
        item = self.item
        self.item, self.timer = None, None
        return item

    def time_text(self, now):
        return f'{self.timer.remaining(now)} SEC' if self.timer else f'{EXPIRE_SECONDS} SEC'

    def process_name(self):
        inside = self.item.name if isinstance(self.item, Ingredient) else f'PLATE #{self.item.number}'
        return f'{self.label} [{inside}]'


class Customer:
    def __init__(self, seat):
        self.seat = seat
        self.label = f'CUSTOMER #{seat}'
        self.order = None
        self.state = 'CLOSED'  # WAITING, EATING, DONE, CLOSED
        self.plate = None
        self.timer = None
        self.order_time = None

    def place(self, order, now):
        self.order = order
        self.state = 'WAITING'
        self.order_time = now

    def serve(self, plate, now, trash):
        self.plate = plate
        self.state = 'EATING'
        self.timer = Timer(now, EAT_SECONDS + penalty(trash))

    def fire(self, game):
        self.state = 'DONE'
        self.timer = None

    def take(self):
        plate = self.plate
        self.plate, self.order, self.state = None, None, 'CLOSED'
        return plate

    def process_name(self):
        return self.label

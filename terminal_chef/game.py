"""Game state and the menu state machine."""

import random
import sys
import time

from . import scores
from .food import FRIDGE, SHELF, Ingredient, Plate, random_orders, recipe_steps
from .render import MARGIN, Box, C, Cells, L, LR, numbered
from .stations import (CUT_SECONDS, WASH_SECONDS, Cooker, Counter, Customer,
                       Disposal, DishWasher, Prepper)

# room id: (title used in ENTERED and IN lines, report name, grid x, grid y)
ROOMS = {
    # Listed across the floor plan, which is also the order the report uses.
    'SERVICE':  ('SERVICE', 'Service', 0, 0),
    'PLATING':  ('PLATING', 'Plating', 0, 1),
    'STOVES':   ('STOVES', 'Stoves', 1, 1),
    'PANTRY':   ('PANTRY', 'Pantry', 2, 1),
    'COUNTERS': ('COUNTERS', 'Counters', 0, 2),
    'PREP':     ('PREP ROOM', 'Prep', 1, 2),
    'CLEANING': ('CLEANING', 'Cleaning', 2, 2),
}
GRID = {(x, y): rid for rid, (_, _, x, y) in ROOMS.items()}
MOVES = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}
TOTAL_ORDERS = 12  # a long game; a short game runs 6
DISTINCT_ORDERS = 8


class ConsoleIO:
    def line(self, text=''):
        sys.stdout.write(text + '\n')
        sys.stdout.flush()

    def raw(self, text):
        sys.stdout.write(text)
        sys.stdout.flush()


class Screen:
    """A menu: `render()` builds its Box, `on_key(key)` reacts to 1-4 or moves."""

    def __init__(self, render, on_key):
        self.render = render
        self.on_key = on_key


def seconds(value):
    return str(int(round(value)))


def clock_text(total):
    minutes, secs = divmod(int(round(total)), 60)
    return f'{minutes} MIN, {secs} SEC'


def fastest_box():
    table = scores.load()
    sections = []
    for mode, heading in (('long', 'LONG GAMES:'), ('short', 'SHORT GAMES:')):
        times = table.get(mode) or []
        rows = [L(f' {heading}')]
        rows += ([LR(numbered(i + 1), clock_text(t)) for i, t in enumerate(times)]
                 or [L('    NONE YET')])
        sections.append(rows)
    return Box('FASTEST GAMES', sections)


def tutorial_box():
    flow = [('BEEF', 'COOK, THEN CUT'), ('CHICKEN', 'WASH, COOK, THEN CUT'),
            ('LETTUCE', 'WASH, THEN CUT'), ('TOMATO', 'WASH, CUT, THEN COOK'),
            ('POTATO', 'CUT, THEN COOK'), ('BREAD', 'CUT')]
    return Box('TUTORIAL', [
        [L(' CONTROLS:'),
         LR('    ARROW KEYS / WASD', 'MOVE BETWEEN ROOMS'),
         LR('    1-4', 'MENU SELECTIONS'),
         LR('    E', 'SHOW EVERYTHING'),
         LR('    R', 'SHOW RECIPES'),
         LR('    ESC', 'PAUSE')],
        [L(' THE KITCHEN:'),
         L('    [SERVICE]'),
         L('    [PLATING] [STOVES]    [PANTRY]'),
         L('    [COUNTERS][PREP ROOM] [CLEANING]')],
        [L(' EVERY DISH:'),
         L('    1. TAKE INGREDIENTS FROM THE PANTRY'),
         L('    2. PREPARE THEM UNTIL THEY READ [RTP]'),
         L('    3. STACK THEM ON A PLATE IN PLATING'),
         L('    4. CARRY THE PLATE TO THE CUSTOMER'),
         L('    5. TAKE THE DIRTY PLATE BACK AND WASH IT')],
        [L(' INGREDIENTS:')] + [L(f'    {name:<10}{steps}') for name, steps in flow],
        [L(' WATCH OUT:'),
         L('    FOOD LEFT COOKING BURNS AND IS LOST'),
         L('    ITEMS LEFT ON COUNTERS EXPIRE'),
         L('    EVERY FINISHED PROCESS ADDS TRASH'),
         L('    AT TRASH 8 AND ABOVE, EVERYTHING SLOWS DOWN')],
    ])


def recipes_box(names):
    sections = [[L(f' {name}:')] + [L(numbered(step, label)) for step, label in recipe_steps(name)]
                for name in names]
    return Box('RECIPES', sections)


class Game:
    def __init__(self, io=None, clock=time.monotonic, rng=random,
                 orders=TOTAL_ORDERS, distinct=DISTINCT_ORDERS, mode='long'):
        self.io = io or ConsoleIO()
        self.clock = clock
        self.rng = rng
        self.trash = 0
        self.inventory = [None, None, None]
        self.plates = [Plate(n) for n in (1, 2, 3)]
        self.plating = list(self.plates)
        self.counters = [Counter(f'COUNTER #{n}') for n in (1, 2, 3)]
        self.cookers = [Cooker('PAN', 'PAN #1'), Cooker('PAN', 'PAN #2'), Cooker('POT', 'POT')]
        self.board = Prepper('CUT', 'CUTTING BOARD', CUT_SECONDS, 'BOARD')
        self.sink = Prepper('WASH', 'SINK', WASH_SECONDS, 'SINK')
        self.washer = DishWasher()
        self.disposal = Disposal()
        self.customers = [Customer(n) for n in (1, 2, 3)]
        # Fixed order for the PROCESSES list; counters have their own section.
        self.processors = (self.cookers + [self.board, self.sink, self.washer, self.disposal]
                           + self.customers)
        self.stations = self.processors + self.counters  # everything that ticks
        self.mode = mode  # 'short' or 'long', for the fastest-games table
        self.total_orders = orders
        self.orders = random_orders(orders, distinct, rng=rng)
        self.next_order = 0
        self.served = []  # (dish name, seconds from order to serve)
        self.room = 'SERVICE'
        self.room_time = {rid: 0.0 for rid in ROOMS}
        self.room_entered_at = None
        self.start_time = None
        self.e_checks = 0
        self.r_checks = 0
        self.disposal_times = []
        self.peek = False  # True while an EVERYTHING or RECIPES menu is showing
        self.math = None  # active multiplication prompt, else None
        self.pause_offset = 0.0  # real seconds spent paused, excluded from game time
        self.paused_at = None  # game time the pause froze at, else None
        self.over = False
        self.quit_early = False  # True when a failed pause ended the run
        self.screen = None

    # ------------------------------------------------------------ basics
    @property
    def now(self):
        """Game time: real time minus every second spent paused. Frozen while paused."""
        if self.paused_at is not None:
            return self.paused_at
        return self.clock() - self.pause_offset

    def add_trash(self, n):
        self.trash = min(10, self.trash + n)

    def show(self, text):
        self.io.line(text)
        self.io.line('')

    def start(self):
        self.start_time = self.room_entered_at = self.now
        for customer in self.customers:
            self.place_order(customer)
        self.go(self.entered_screen())

    def tick(self):
        """Fire every due timer in chronological order."""
        now = self.now
        while True:
            due = [(s.timer.end, i, s) for i, s in enumerate(self.stations)
                   if s.timer is not None and s.timer.end <= now]
            if not due:
                return
            due.sort(key=lambda d: d[:2])
            due[0][2].fire(self)

    def render(self):
        self.tick()
        self.show(self.screen.render().render())

    def go(self, screen):
        self.screen = screen
        self.render()

    # ------------------------------------------------------------ input
    def press(self, key):
        if self.over:
            return
        self.tick()
        if self.math is not None:
            self.math_key(key)
        elif self.peek:
            # While peeking, any recognised key just closes the peek and is consumed.
            self.peek = False
            self.render()
        elif key == 'E':
            self.peek = True
            self.e_checks += 1
            self.show(self.everything_box().render())
        elif key == 'R':
            self.peek = True
            self.r_checks += 1
            self.show(recipes_box(self.outstanding()).render())
        elif key == 'ESC':
            self.pause()
        else:
            self.screen.on_key(key)

    def move(self, direction):
        _, _, x, y = ROOMS[self.room]
        dx, dy = MOVES[direction]
        target = GRID.get((x + dx, y + dy))
        if target is None:
            return
        now = self.now
        self.room_time[self.room] += now - self.room_entered_at
        self.room_entered_at = now
        self.room = target
        self.go(self.entered_screen())

    # ------------------------------------------------------------ shared pieces
    def inventory_lines(self):
        return [L(numbered(i + 1, item.label if item else '')) for i, item in enumerate(self.inventory)]

    def customer_section(self):
        now = self.now
        rows = [L(' CUSTOMER STATUS:')]
        for c in self.customers:
            left = f'    #{c.seat}: {c.state}'
            if c.state == 'WAITING':
                rows.append(LR(left, c.order))
            elif c.state == 'EATING':
                rows.append(LR(left, f'{c.timer.remaining(now)} SEC'))
            else:
                rows.append(L(left))
        return rows

    def outstanding(self):
        return [c.order for c in self.customers if c.state == 'WAITING']

    def head_line(self, label, station, now):
        """'  PAN #2: Beef' with its time right-aligned, for a room status line."""
        content, right = station.head(now)
        left = f'{label} {content}'
        return LR(left, right) if right else L(left)

    def take_status(self, station):
        item = station.item
        if item is None:
            return C('EMPTY')
        time_text = station.time_text(self.now)
        return LR('  ' + item.label, time_text) if time_text else C(item.label)

    def picker(self, title, status, on_pick, back):
        """A PICK INVENTORY SLOT menu. `status` builds the optional status line,
        `on_pick(slot)` returns True on success, `back()` builds the RETURN target."""
        def render():
            sections = []
            line = status() if status else None
            if line is not None:
                sections.append([line])
            sections.append([L(' PICK INVENTORY SLOT:')] + self.inventory_lines()
                            + [L(numbered(4, 'RETURN'))])
            return Box(title, sections)

        def on_key(key):
            if key in ('1', '2', '3'):
                if on_pick(int(key) - 1) and not self.over:
                    self.go(self.entered_screen())
            elif key == '4':
                self.go(back())

        return Screen(render, on_key)

    # ------------------------------------------------------------ ENTERED menus
    def entered_screen(self):
        room = self.room
        select = {
            'SERVICE': self.service_select, 'PLATING': self.plating_select,
            'COUNTERS': self.counters_select, 'STOVES': self.stoves_select,
            'PREP': self.prep_select, 'PANTRY': self.pantry_select,
            'CLEANING': self.cleaning_select,
        }[room]

        def on_key(key):
            if key in MOVES:
                self.move(key)
            elif key in ('1', '2', '3'):
                select(int(key))

        return Screen(lambda: self.entered_box(room), on_key)

    def entered_box(self, room):
        title = f'ENTERED: {ROOMS[room][0]}'
        now = self.now
        interact = [L(' INTERACT W/:')]
        if room == 'SERVICE':
            return Box(title, [self.customer_section(),
                               interact + [L(numbered(c.seat, c.label)) for c in self.customers]])
        if room == 'PLATING':
            slots = [L(numbered(i + 1, p.label if p else '')) for i, p in enumerate(self.plating)]
            return Box(title, [self.customer_section(), interact + slots])
        if room == 'COUNTERS':
            rows = [LR(f'    #{i + 1}: {c.item.label}', c.time_text(now)) if c.item else L(f'    #{i + 1}:')
                    for i, c in enumerate(self.counters)]
            return Box(title, [rows, interact + [L(numbered(i + 1, c.label)) for i, c in enumerate(self.counters)]])
        if room == 'STOVES':
            pad = max(len(c.label) for c in self.cookers)  # right-align PAN #1 / PAN #2 / POT
            rows = [self.head_line(f'  {c.label:>{pad}}:', c, now) for c in self.cookers]
            return Box(title, [rows,
                               interact + [L(numbered(i + 1, c.label)) for i, c in enumerate(self.cookers)]])
        if room == 'PREP':
            preppers = (self.board, self.sink)
            pad = max(len(s.short) for s in preppers)  # right-align BOARD / SINK
            rows = [self.head_line(f'  {s.short:>{pad}}:', s, now) for s in preppers]
            return Box(title, [rows,
                               interact + [L(numbered(1, 'CUTTING BOARD')), L(numbered(2, 'SINK'))]])
        if room == 'PANTRY':
            return Box(title, [interact + [L(numbered(1, 'FRIDGE')), L(numbered(2, 'SHELF'))]])
        return Box(title, [[Cells(f'WASHER: {self.washer.status_short(now)}',
                                  f'DISPOSAL: {self.disposal.status(now)}')],
                           interact + [L(numbered(1, 'DISH WASHER')), L(numbered(2, 'TRASH DISPOSAL')),
                                       L(numbered(3, 'DISCARD BIN'))]],
                   title_extra=[f'TRASH LEVEL: {self.trash}'])

    # ------------------------------------------------------------ SERVICE
    def service_select(self, n):
        customer = self.customers[n - 1]
        if customer.state == 'WAITING':
            self.go(self.picker([customer.label, 'SERVE FOOD'], lambda: C(f'ORDER: {customer.order}'),
                                lambda i: self.serve(customer, i), self.entered_screen))
        elif customer.state == 'DONE':
            self.go(self.picker([customer.label, 'TAKE PLATE'], None,
                                lambda i: self.take_plate(customer, i), self.entered_screen))

    def serve(self, customer, i):
        item = self.inventory[i]
        if not isinstance(item, Plate) or item.dirty or item.dish_name() != customer.order:
            return False
        now = self.now
        self.inventory[i] = None
        self.served.append((customer.order, now - customer.order_time))
        customer.serve(item, now, self.trash)
        self.show(Box(f'SERVED {customer.label}').render())
        if len(self.served) == self.total_orders:
            self.finish()
        return True

    def take_plate(self, customer, i):
        if self.inventory[i] is not None:
            return False
        plate = customer.take()
        plate.soil()
        self.inventory[i] = plate
        self.add_trash(1)
        order = self.place_order(customer)
        if order:
            self.show(Box(f'NEW ORDER: {order}').render())
        return True

    def place_order(self, customer):
        if self.next_order >= len(self.orders):
            return None
        order = self.orders[self.next_order]
        self.next_order += 1
        customer.place(order, self.now)
        return order

    # ------------------------------------------------------------ PLATING
    def plating_select(self, n):
        slot = n - 1
        if self.plating[slot] is None:
            self.go(self.picker([f'SLOT #{n}', 'ADD PLATE'], None,
                                lambda i: self.add_plate(slot, i), self.entered_screen))
        else:
            self.go(self.plate_screen(slot))

    def plate_screen(self, slot):
        plate = self.plating[slot]
        title = f'PLATE #{plate.number}'
        status = lambda: C(plate.content or 'EMPTY')

        def render():
            return Box(title, [[status()], [L(' ACTION:'), L(numbered(1, 'ADD INGREDIENT')),
                                            L(numbered(2, 'PICK UP PLATE')), L(numbered(4, 'RETURN'))]])

        def on_key(key):
            if key == '1':
                self.go(self.picker([title, 'ADD INGREDIENT'], status,
                                    lambda i: self.add_ingredient(plate, i), lambda: self.plate_screen(slot)))
            elif key == '2':
                self.go(self.picker([title, 'MOVE TO INVENTORY'], status,
                                    lambda i: self.pick_up_plate(slot, i), lambda: self.plate_screen(slot)))
            elif key == '4':
                self.go(self.entered_screen())

        return Screen(render, on_key)

    def add_plate(self, slot, i):
        item = self.inventory[i]
        if not isinstance(item, Plate) or item.dirty:
            return False
        self.plating[slot], self.inventory[i] = item, None
        return True

    def add_ingredient(self, plate, i):
        item = self.inventory[i]
        if not isinstance(item, Ingredient) or not plate.can_add(item):
            return False
        plate.add(item)
        self.inventory[i] = None
        return True

    def pick_up_plate(self, slot, i):
        if self.inventory[i] is not None:
            return False
        self.inventory[i], self.plating[slot] = self.plating[slot], None
        return True

    # ------------------------------------------------------------ COUNTERS
    def counters_select(self, n):
        counter = self.counters[n - 1]
        if counter.item is None:
            self.go(self.picker([counter.label, 'STORE ITEM'], lambda: C('EMPTY'),
                                lambda i: self.store_item(counter, i), self.entered_screen))
        else:
            self.go(self.picker([counter.label, 'TAKE ITEM'], lambda: self.take_status(counter),
                                lambda i: self.take_from(counter, i), self.entered_screen))

    def store_item(self, counter, i):
        item = self.inventory[i]
        if item is None or counter.item is not None:
            return False
        counter.store(item, self.now)
        self.inventory[i] = None
        return True

    def take_from(self, station, i):
        if self.inventory[i] is not None or not station.can_take():
            return False
        self.inventory[i] = station.take()
        return True

    def add_to(self, station, i):
        item = self.inventory[i]
        if not isinstance(item, Ingredient) or not station.accepts(item):
            return False
        station.start(item, self.now, self.trash)
        self.inventory[i] = None
        return True

    # ------------------------------------------------------------ STOVES / PREP
    def stoves_select(self, n):
        # Pans and the pot use a single-segment title, unlike the prep stations.
        self.station_select(self.cookers[n - 1], segments=False)

    def prep_select(self, n):
        if n <= 2:
            self.station_select([self.board, self.sink][n - 1])

    def station_select(self, station, segments=True):
        if not station.selectable:
            return
        taking = station.item is not None
        title = [station.label]
        if segments:
            title.append('TAKE ITEM' if taking else 'ADD ITEM')
        status = (lambda: self.take_status(station)) if taking else (lambda: C('EMPTY'))
        action = (lambda i: self.take_from(station, i)) if taking else (lambda i: self.add_to(station, i))
        self.go(self.picker(title, status, action, self.entered_screen))

    # ------------------------------------------------------------ PANTRY
    def pantry_select(self, n):
        if n == 1:
            self.go(self.pantry_screen('IN THE FRIDGE', FRIDGE))
        elif n == 2:
            self.go(self.pantry_screen('ON THE SHELF', SHELF))

    def pantry_screen(self, title, names):
        def render():
            return Box(title, [[L(' SELECT:')] + [L(numbered(i + 1, name)) for i, name in enumerate(names)]
                               + [L(numbered(4, 'RETURN'))]])

        def on_key(key):
            if key in ('1', '2', '3'):
                name = names[int(key) - 1]
                self.go(self.picker([f'SELECTED {name.upper()}'], None,
                                    lambda i: self.grab(name, i), lambda: self.pantry_screen(title, names)))
            elif key == '4':
                self.go(self.entered_screen())

        return Screen(render, on_key)

    def grab(self, name, i):
        if self.inventory[i] is not None:
            return False
        self.inventory[i] = Ingredient(name)
        return True

    # ------------------------------------------------------------ CLEANING
    def cleaning_select(self, n):
        if n == 1:
            if self.washer.running:
                return
            # Clean plates mean taking is the only useful action, so skip the action menu.
            self.go(self.washer_take_screen() if self.washer.clean_plates() else self.washer_screen())
        elif n == 2:
            if not self.disposal.running:
                self.start_math(['TRASH DISPOSAL', 'ACTIVATE'], 3,
                                'STARTED TRASH DISPOSAL', self.disposal_activated)
        elif n == 3:
            self.go(self.picker(['DISCARD BIN'], None, self.discard, self.entered_screen))

    def washer_status(self):
        return C(self.washer.status_long(self.now))

    def washer_take_screen(self):
        return self.picker(['DISH WASHER', 'TAKE PLATE'], self.washer_status,
                           self.washer_take, self.entered_screen)

    def washer_screen(self):
        """The action menu, reached only while the washer is empty or holds dirty plates."""
        def render():
            return Box('DISH WASHER', [[self.washer_status()],
                                       [L(' ACTION:'), L(numbered(1, 'ADD PLATE')),
                                        L(numbered(2, 'START WASHER')), L(numbered(4, 'RETURN'))]])

        def on_key(key):
            if key == '1':
                self.go(self.picker(['DISH WASHER', 'ADD PLATE'], self.washer_status,
                                    self.washer_add, self.washer_screen))
            elif key == '2':
                if self.washer.start(self.now, self.trash):
                    self.show(Box('STARTED DISH WASHER').render())
                    self.go(self.entered_screen())
            elif key == '4':
                self.go(self.entered_screen())

        return Screen(render, on_key)

    def washer_add(self, i):
        item = self.inventory[i]
        if not isinstance(item, Plate) or not self.washer.can_add():
            return False
        self.washer.add(item)
        self.inventory[i] = None
        return True

    def washer_take(self, i):
        if self.inventory[i] is not None or not self.washer.clean_plates():
            return False
        self.inventory[i] = self.washer.retrieve()
        return True

    def discard(self, i):
        item = self.inventory[i]
        if item is None:
            return False
        if isinstance(item, Plate):
            if not item.items:
                return False  # plates themselves can never be thrown away
            item.soil()
        else:
            self.inventory[i] = None
        return True

    # ------------------------------------------------------------ multiplication prompts
    def start_math(self, segments, needed, footer, on_done, cursor=True, on_wrong=None):
        """Open a multiplication challenge below an open-bottomed title box.

        `needed` correct answers finish it, printing `footer` and calling
        `on_done(started)`. A wrong answer calls `on_wrong()` if given,
        otherwise it simply poses a fresh problem.
        """
        self.math = {'correct': 0, 'needed': needed, 'typed': '', 'answer': None,
                     'started': self.now, 'cursor': cursor, 'footer': footer,
                     'on_done': on_done, 'on_wrong': on_wrong}
        title = '||'.join(f'  {s}  ' for s in segments)
        self.io.line(MARGIN + '//' + '=' * len(title) + '\\\\')
        self.io.line(MARGIN + '||' + title + '||')
        self.io.line(MARGIN + '||' + '=' * len(title) + '//')
        self.new_problem()

    def new_problem(self):
        a, b = self.rng.randint(1, 9), self.rng.randint(1, 9)
        self.math['answer'] = a * b
        self.math['typed'] = ''
        # The underscore is a cursor the first typed digit overwrites.
        tail = '_\b' if self.math['cursor'] else ''
        self.io.raw(f'{MARGIN}||  {a} X {b} = {tail}')

    def math_key(self, key):
        m = self.math
        if key.isdigit():
            if len(m['typed']) < 3:
                m['typed'] += key
                self.io.raw(key)
        elif key == 'BACKSPACE':
            if m['typed']:
                m['typed'] = m['typed'][:-1]
                blank = m['cursor'] and not m['typed']
                self.io.raw('\b_\b' if blank else '\b \b')
        elif key == 'ENTER':
            self.io.raw('\n')
            if not (m['typed'] and int(m['typed']) == m['answer']):
                if m['on_wrong'] is not None:
                    self.math = None
                    m['on_wrong']()
                    return
            else:
                m['correct'] += 1
            if m['correct'] < m['needed']:
                self.new_problem()
                return
            self.math = None
            self.show_footer(m['footer'])
            m['on_done'](m['started'])

    def show_footer(self, text):
        """A small box that hangs off the bottom of a multiplication prompt."""
        width = len(text) + 4
        self.io.line(MARGIN + '||' + '=' * width + '\\\\')
        self.io.line(MARGIN + f'||  {text}  ||')
        self.io.line(MARGIN + '\\\\' + '=' * width + '//')
        self.io.line('')

    def disposal_activated(self, started):
        self.disposal_times.append(self.now - started)
        self.disposal.start(self.now, self.trash)
        self.go(self.entered_screen())

    # ------------------------------------------------------------ pause
    def pause(self):
        """ESC freezes game time behind one multiplication. Wrong answer ends the run."""
        if self.over or self.paused_at is not None:
            return
        self.paused_at = self.now
        self.start_math(['GAME PAUSED', 'RESUME:'], 1, 'CONTINUE!',
                        self.resume, on_wrong=self.fail_pause)

    def resume(self, started):
        self.pause_offset = self.clock() - self.paused_at
        self.paused_at = None
        self.render()  # reprint whichever menu they were on

    def fail_pause(self):
        self.paused_at = None
        self.quit_early = True
        self.over = True
        self.show_footer('GAME OVER')

    # ------------------------------------------------------------ EVERYTHING / report
    def everything_box(self):
        now = self.now
        orders = [L(numbered(c.seat, c.order)) for c in self.customers if c.state == 'WAITING']
        counters = [LR(numbered(i + 1, c.item.label), c.time_text(now)) if c.item else L(numbered(i + 1))
                    for i, c in enumerate(self.counters)]
        processes = [(s.process_name(), s.timer.remaining(now)) for s in self.processors if s.timer is not None]
        process_lines = [LR(numbered(i + 1, name), f'{t} SEC') for i, (name, t) in enumerate(processes)]
        return Box('EVERYTHING', [
            [Cells(f'IN: {ROOMS[self.room][0]}', f'TRASH LVL: {self.trash}')],
            [L(' OUTSTANDING ORDERS:')] + orders,
            [L(' INVENTORY:')] + self.inventory_lines(),
            [L(' COUNTERS:')] + counters,
            [L(' PROCESSES:')] + process_lines,
        ])

    def finish(self):
        now = self.now
        self.room_time[self.room] += now - self.room_entered_at
        self.over = True
        scores.record(self.mode, now - self.start_time)
        self.show(self.report_box(now).render())

    def report_box(self, now):
        elapsed = clock_text(now - self.start_time)
        dishes = [LR(numbered(i + 1, name), f'{seconds(t)} SEC') for i, (name, t) in enumerate(self.served)]
        rooms = [LR(f'    {ROOMS[rid][1]}', f'{seconds(self.room_time[rid])} SEC') for rid in ROOMS]
        avg_dish = sum(t for _, t in self.served) / len(self.served) if self.served else 0
        avg_disposal = sum(self.disposal_times) / len(self.disposal_times) if self.disposal_times else 0
        stats = [LR(numbered(1, 'AVERAGE TIME PER DISH:'), f'{seconds(avg_dish)} SEC'),
                 LR(numbered(2, 'AVERAGE DISPOSAL ACTIVATION:'), f'{seconds(avg_disposal)} SEC'),
                 LR(numbered(3, '# OF EVERYTHING CHECKS:'), str(self.e_checks)),
                 LR(numbered(4, '# OF RECIPE CHECKS:'), str(self.r_checks))]
        return Box('GAME REPORT', [
            [C(f'YOU SERVED {len(self.served)} CUSTOMERS IN: {elapsed}')],
            [L(' DISHES SERVED:')] + dishes,
            [L(' TIME SPENT IN:')] + rooms,
            [L(' STATISTICS:')] + stats,
        ])

"""Ingredients, plates, and recipes."""

import random
from collections import Counter

TAG = {'WASH': '[UNWASHED]', 'CUT': '[UNCUT]', 'COOK': '[UNCOOKED]'}

# name: (processing steps in order, steps done before [RTP] appears, cook seconds, vessel)
INGREDIENTS = {
    'Beef':    (('COOK', 'CUT'), 1, 25, 'PAN'),
    'Chicken': (('WASH', 'COOK', 'CUT'), 2, 20, 'PAN'),
    'Lettuce': (('WASH', 'CUT'), 2, None, None),
    'Tomato':  (('WASH', 'CUT', 'COOK'), 2, 15, 'POT'),
    'Potato':  (('CUT', 'COOK'), 2, 15, 'POT'),
    'Bread':   (('CUT',), 0, None, None),
}
FRIDGE = ['Beef', 'Chicken', 'Lettuce']
SHELF = ['Tomato', 'Potato', 'Bread']


def label_for(key):
    name, done = key
    steps, rtp_at, _, _ = INGREDIENTS[name]
    tags = [TAG[s] for s in steps[done:]]
    if done >= rtp_at:
        tags.append('[RTP]')
    return ' '.join(tags + [name])


class Ingredient:
    def __init__(self, name, done=0):
        self.name = name
        self.done = done  # number of processing steps completed

    @property
    def key(self):
        return (self.name, self.done)

    @property
    def next_step(self):
        steps = INGREDIENTS[self.name][0]
        return steps[self.done] if self.done < len(steps) else None

    @property
    def is_rtp(self):
        return self.done >= INGREDIENTS[self.name][1]

    @property
    def cook_seconds(self):
        return INGREDIENTS[self.name][2]

    @property
    def vessel(self):
        return INGREDIENTS[self.name][3]

    @property
    def label(self):
        return label_for(self.key)

    def advance(self):
        self.done += 1


# Ingredient states used by recipes: (name, steps done)
BREAD_RTP, BREAD_UNCUT = ('Bread', 1), ('Bread', 0)
PATTY, STEAK = ('Beef', 1), ('Beef', 2)
CHICKEN_PATTY, CHICKEN_CUT = ('Chicken', 2), ('Chicken', 3)
LETTUCE = ('Lettuce', 2)
TOMATO_RAW, TOMATO_COOKED = ('Tomato', 2), ('Tomato', 3)
POTATO = ('Potato', 2)


def _sandwiches(base, meat):
    return [
        (base, [[BREAD_RTP], [meat]]),
        (f'{base} w/ Lettuce', [[BREAD_RTP], [meat], [LETTUCE]]),
        (f'{base} w/ Tomato', [[BREAD_RTP], [meat], [TOMATO_RAW]]),
        (f'{base} w/ Lettuce & Tomato', [[BREAD_RTP], [meat], [LETTUCE, TOMATO_RAW]]),
    ]


# Each recipe is (dish name, step groups). Items inside one group share a step
# number and may be added in any order; groups must be completed in order.
RECIPES = [
    *_sandwiches('Burger', PATTY),
    *_sandwiches('Chicken Sandwich', CHICKEN_PATTY),
    ('Steak', [[STEAK]]),
    ('Steak w/ Mashed Potatos', [[STEAK], [POTATO]]),
    ('Chicken', [[CHICKEN_CUT]]),
    ('Chicken w/ Mashed Potatos', [[CHICKEN_CUT], [POTATO]]),
    ('Potato Soup', [[POTATO], [BREAD_UNCUT]]),
    ('Potato Soup w/ Beef', [[POTATO], [BREAD_UNCUT], [STEAK]]),
    ('Potato Soup w/ Chicken', [[POTATO], [BREAD_UNCUT], [CHICKEN_CUT]]),
    ('Tomato Soup', [[TOMATO_COOKED], [BREAD_UNCUT]]),
    ('Salad', [[LETTUCE], [TOMATO_RAW]]),
    ('Salad w/ Extra Tomato', [[LETTUCE], [TOMATO_RAW, TOMATO_RAW]]),
    ('Steak Salad', [[LETTUCE], [TOMATO_RAW, STEAK]]),
    ('Steak Salad w/ Extra Tomato', [[LETTUCE], [TOMATO_RAW, STEAK, TOMATO_RAW]]),
    ('Chicken Salad', [[LETTUCE], [TOMATO_RAW, CHICKEN_CUT]]),
    ('Chicken Salad w/ Extra Tomato', [[LETTUCE], [TOMATO_RAW, CHICKEN_CUT, TOMATO_RAW]]),
]
RECIPE_BY_NAME = dict(RECIPES)
DISH_NAMES = [name for name, _ in RECIPES]


def recipe_steps(name):
    """[(step number, ingredient label)] for the RECIPES view."""
    return [(i + 1, label_for(key)) for i, group in enumerate(RECIPE_BY_NAME[name]) for key in group]


def match(sequence, groups):
    """'complete' if the sequence is exactly the recipe, 'prefix' if it could
    still become it, None if it can never become it."""
    i = 0
    for group in groups:
        need = Counter(group)
        while need:
            if i == len(sequence):
                return 'prefix'
            key = sequence[i]
            if need[key] <= 0:
                return None
            need[key] -= 1
            if need[key] == 0:
                del need[key]
            i += 1
    return 'complete' if i == len(sequence) else None


class Plate:
    def __init__(self, number):
        self.number = number
        self.dirty = False
        self.items = []

    @property
    def sequence(self):
        return [item.key for item in self.items]

    def dish_name(self):
        for name, groups in RECIPES:
            if match(self.sequence, groups) == 'complete':
                return name
        return None

    def can_add(self, ingredient):
        if self.dirty or not ingredient.is_rtp:
            return False
        sequence = self.sequence + [ingredient.key]
        return any(match(sequence, groups) for _, groups in RECIPES)

    def add(self, ingredient):
        self.items.append(ingredient)

    def soil(self):
        """Discard any food and mark the plate dirty."""
        self.items = []
        self.dirty = True

    @property
    def content(self):
        return self.dish_name() or ', '.join(item.name for item in self.items)

    @property
    def label(self):
        if self.dirty:
            return f'[DIRTY] [PLATE #{self.number}]'
        return f'[PLATE #{self.number}] {self.content}'.rstrip()


def random_orders(count=12, distinct=8, rng=random):
    distinct = min(distinct, count)
    while True:
        orders = [rng.choice(DISH_NAMES) for _ in range(count)]
        if len(set(orders)) >= distinct:
            return orders

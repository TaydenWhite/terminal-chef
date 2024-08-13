from Item import Ingredient
from Item import Item

class Room:
    def __init__(self, name):
        self.action1 = Action()
        self.action2 = Action()
        self.action_states = [1, 2]

    def __str__(self):
        pass

# PANTRY CLASS
class Pantry():
    
    def __init__(self):
        fridge = ['Beef', 'Chicken', 'Lettuce']
        self.beef = Ingredient('Beef', {'[RTP]' : False, '[UNWASHED]' : False, 
                                        '[UNCUT]' : True, '[UNCOOKED]' : True, '[BURNED]' : False}, False)
        self.chicken = Ingredient('Chicken', {'[RTP]' : False, '[UNWASHED]' : True, 
                                        '[UNCUT]' : False, '[UNCOOKED]' : True, '[BURNED]' : False}, False)
        self.lettuce = Ingredient('Lettuce', {'[RTP]' : False, '[UNWASHED]' : True, 
                                        '[UNCUT]' : True, '[UNCOOKED]' : False, '[BURNED]' : False}, False)
        self.tomato = Ingredient('Tomato', {'[RTP]' : False, '[UNWASHED]' : True, 
                                        '[UNCUT]' : True, '[UNCOOKED]' : True, '[BURNED]' : False}, False)
        self.potato = Ingredient('Potato', {'[RTP]' : False, '[UNWASHED]' : True, 
                                        '[UNCUT]' : True, '[UNCOOKED]' : True, '[BURNED]' : False}, False)
        self.bread = Ingredient('Bread', {'[RTP]' : True, '[UNWASHED]' : False, 
                                        '[UNCUT]' : False, '[UNCOOKED]' : False, '[BURNED]' : False}, False)
        
        self.fridge = [self.beef, self.chicken, self.lettuce]
        self.shelf = [self.tomato, self.potato, self.bread]

class Plating():

    def __unit__(self):
        self.plate1 = Item([], [], [], 1, 'plating')
        self.plate2 = Item([], [], [], 2, 'plating')
        self.plate3 = Item([], [], [], 3, 'plating')

class Prep():
    
    def __init__(self):
        self.fridge = ['Beef', 'Chicken', 'Lettuce']
        self.shelf = ['Tomato', 'Potato', 'Bread']
        self.state = 0
        self.room_state = 0
        self.action_states = [1, 2]

class Action:
    def __init__(self, name, item, time):
        self.name = name
        self.item = item
        self.time = time


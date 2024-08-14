from Ingredient import Ingredient
from Item import Item




# PANTRY CLASS
class Pantry():
    def __init__(self):

        beef = Ingredient('Beef', {'[RTP]' : False, '[UNWASHED]' : False, 
                                   '[UNCUT]' : True, '[UNCOOKED]' : True, '[BURNED]' : False}, False)
        chicken = Ingredient('Chicken', {'[RTP]' : False, '[UNWASHED]' : True, 
                                         '[UNCUT]' : False, '[UNCOOKED]' : True, '[BURNED]' : False}, False)
        lettuce = Ingredient('Lettuce', {'[RTP]' : False, '[UNWASHED]' : True, 
                                         '[UNCUT]' : True, '[UNCOOKED]' : False, '[BURNED]' : False}, False)
        tomato = Ingredient('Tomato', {'[RTP]' : False, '[UNWASHED]' : True, 
                                       '[UNCUT]' : True, '[UNCOOKED]' : True, '[BURNED]' : False}, False)
        potato = Ingredient('Potato', {'[RTP]' : False, '[UNWASHED]' : True, 
                                       '[UNCUT]' : True, '[UNCOOKED]' : True, '[BURNED]' : False}, False)
        bread = Ingredient('Bread', {'[RTP]' : True, '[UNWASHED]' : False, 
                                     '[UNCUT]' : False, '[UNCOOKED]' : False, '[BURNED]' : False}, False)
        
        self.fridge = [beef, chicken, lettuce]
        self.shelf = [tomato, potato, bread]

    def __str__(self):
        return '\t//===================\\\\\n\t||  ENTERED: PANTRY  ||\n\t||===================||\n\t|| INTERACT W/:      ||\n\t||    1. FRIDGE      ||\n\t||    2. SHELF       ||\n\t\\\\===================//'

class Plating():

    def __init__(self):
        self.plates = [Item([], [], [], 1, 'plating', False), 
                        Item([], [], [], 2, 'plating', False),
                        Item([], [], [], 3, 'plating', False)]

    def __str__(self, game):
        string = ''
        
        return string
    
#   //=========================\\
#   ||  ENTERED: PLATING ROOM  ||
#   ||==============================================\\
#   || CUSTOMER STATUS:                             ||
#   ||      1. Burger w/ Tomato & Lettuce           ||
#   ||      2. EATING              7 SEC REMAINING  ||
#   ||      3. DONE                                 ||
#   ||==============================================||
#   || INTERACT W/:                                 ||
#   ||    1. [PLATE #1] Burger w/ Tomato & Lettuce  || 
#   ||    2.                                        ||
#   ||    3. PLATE #3                               ||   
#   \\==============================================//


        




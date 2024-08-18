import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Ingredient import Ingredient

class Plate:
    def __init__(self, mains, withs, sides, plate_num, show_plate):
        self.mains = mains # main ingredients ------- beef, bread for burger
        self.withs = withs # additional ingredients - tomato, lettuce for burger 
        self.sides = sides # side dish ingredients -- fries for burger
        self.plate_num = plate_num
        self.show_plate = show_plate # show in inventory -- not in orders
        self.dirty = False

    def add_ingredient(self, ingredient: Ingredient, loc):

        dish_map = {['Tomato'] : ['Tomato Soup'], 
                    ['Potato'] : ['French Fries'], 
                    ['Bread', 'Beef'] : ['Burger'],
                    ['Bread', 'Chicken', 'Tomato'] : ['Chicken Parm'], 
                    ['Lettuce'] : ['Salad'], 
                    ['Beef'] : ['Steak']}
        
        if not ingredient.get_tags()['[RTP]']: return 'NOT READY'
    
        if loc == 1: (self.mains).append(ingredient)
        elif loc == 2: (self.withs).append(ingredient)
        elif loc == 3: (self.sides).append(ingredient)

        if self.mains in dish_map: self.mains = dish_map[self.mains]
        if self.sides in dish_map: self.sides = dish_map[self.sides]
        
        return 'SUCCESS'        

    def __str__(self):
        string = ''

        if self.dirty: string += '[DIRTY] '
        if self.show_plate: string += f'[PLATE #{self.plate_num}] '

        if self.mains:
            for index, main in enumerate(self.mains):
                string += f'{main}'
                if index < len(self.mains) - 1: string += ', '
            
        if self.withs:
            string += ' w/ '
            for index, topping in enumerate(self.withs):
                string += f'{topping}'
                if index < len(self.withs) - 1: string += ', '
                    
        if self.sides:
            string += ' & '
            for index, side in enumerate(self.sides):
                string += f'{side}'
                if index < len(self.withs) - 1: string += ', '

        return string
    

    def get_mains(self): return self.mains
    def get_withs(self): return self.withs
    def get_sides(self): return self.sides
    def get_plate_num(self): return self.plate_num
    
    def set_mains(self, mains): self.mains = mains
    def set_withs(self, withs): self.withs = withs
    def set_sides(self, sides): self.sides = sides
    def set_plate_num(self, plate_num): self.plate_num = plate_num
    def set_show_plate(self, show_plate): self.show_plate = show_plate
    
    def switch_dirty(self):
        self.dirty = not self.dirty
    



             
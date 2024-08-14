from Ingredient import Ingredient

class Item:
    def __init__(self, plate_num, mains, withs, sides, location, empty):
        self.mains = mains # main ingredients ------- beef, bread for burger
        self.withs = withs # additional ingredients - tomato, lettuce for burger 
        self.sides = sides # side dish ingredients -- fries for burger
        self.plate_num = plate_num
        self.loc = location # can be "inventory", "plating", "order" -- used to determine print format
        self.empty = empty # empty plate when plate_num is 0, empty slot when not
        self.dirty = False
        

    def __str__(self):

        if self.empty and self.plate_num == 0: return ''
        if self.empty and self.plate_num != 0:
            if self.dirty: return f'[DIRTY] Plate #{self.plate_num}'
            else: return f'[DIRTY] Plate #{self.plate_num}'

        dish_map = {['Tomato'] : 'Tomato Soup', ['Potato'] : 'French Fries', ['Bread', 'Beef'] : 'Burger',
                    ['Bread', 'Chicken', 'Tomato'] : 'Chicken Parm', ['Lettuce'] : 'Salad', ['Beef'] : 'Steak'}

        if self.loc in ['inventory', 'plating']: string = f'[PLATE #{self.plate_num}] '
        
        # printing item ingredients
        if self.mains in dish_map: string += f'{dish_map[self.mains]}'
        else:
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
    
    def item_merge(self, item2):
        item1 = self
        merge_item = item1

        if type(item2) == Ingredient:
            if (item2.get_tags())['[RTP]']:
                # if main ingredient already maps to a dish -> 

        elif type(item2) == Item:
            pass
        

        return merge_item
    
    def get_mains(self):
        return self.mains
    def get_withs(self):
        return self.withs
    def get_sides(self):
        return self.sides
    def get_plate_num(self):
        return self.plate_num
    def get_loc(self):
        return self.loc
    def get_empty(self):
        return self.empty
    
    def set_mains(self, mains):
        self.mains = mains
    def set_withs(self, withs):
        self.withs = withs
    def set_sides(self, sides):
        self.sides = sides
    def set_plate_num(self, plate_num):
        self.plate_num = plate_num
    def set_loc(self, loc):
        self.loc = loc
    def set_empty(self, empty):
        self.empty = empty
    



             
class Item:
    def __init__(self, plate_num, mains, withs, sides, location):
        self.mains = mains # main ingredients ------- beef, bread for burger
        self.withs = withs # additional ingredients - tomato, lettuce for burger 
        self.sides = sides # side dish ingredients -- fries for burger
        self.plate_num = plate_num
        self.loc = location # can be "inventory", "plating", "order" -- used to determine print format
        
        

    def __str__(self):

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



            pass
        elif type(item2) == Item:
            pass
        

        return merge_item

# ingredients are: Tomato, Potato, Lettuce, Beef, Chicken, Bread
class Ingredient:
    def __init__(self, name, tags, show_tags):
        self.name = name
        self.tags = tags
        self.show_tags = show_tags # only show tags in inventory 

        # example tags input
        # tags = {'[RTP]' : False, '[UNWASHED]' : True, 
        #        '[UNCUT]' : False, '[UNCOOKED]' : True, '[BURNED]' : False}

    def __str__(self):
        string = ''
        
        if self.show_tags:
            for tag in self.tags:
                if self.tags[tag]: string += f'{tag} '
            string += self.name

        return string
             
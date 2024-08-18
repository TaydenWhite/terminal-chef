from Data.Items.Ingredient import Ingredient

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

    def get_item(self, choice, loc): # location is the current state of the room
        if loc == 1: return (self.fridge)[choice - 1]
        elif loc == 2: return (self.shelf)[choice - 1]

    



class Room:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        pass

# PANTRY CLASS
class Pantry():

#   //===================\\
#   ||  ENTERED: PANTRY  ||
#   ||===================||
#   || INTERACT W/:      ||
#   ||    1. FRIDGE      ||
#   ||    2. SHELF       ||
#   \\===================//
    
    def action_menu(self):
        print("//===================\\\\\n\t||  ENTERED: PANTRY  ||\n\t||===================||\n\t|| INTERACT W/:      ||\n\t||    1. FRIDGE      ||\n\t||    2. SHELF       ||\n\t\\===================//")

    def fridge_menu(self):
        print("//=================\\\\\n\t||  IN THE FRIDGE  ||\n\t||=================||\n\t|| SELECT:         ||\n\t||    1. BEEF      ||\n\t||    2. CHICKEN   ||\n\t||    3. LETTUCE   ||\n\t\\=================//\n\t")

    def shelf_menu(self):
//================\\
||  ON THE SHELF  ||
||================||
|| SELECT:        ||
||    1. TOMATO   ||
||    2. POTATO   ||
||    3. BREAD    ||
\\================//

    def __init__(self):
        self.fridge = ['Beef', 'Chicken', 'Lettuce']
        self.shelf = ['Tomato', 'Potato', 'Bread']
        self.state = 0
        

    def menu(self, game):
        pass



    


# PREP ROOM CLASS
# STOVES CLASS
# PANTRY CLASS
# PANTRY CLASS
# PANTRY CLASS


class Action:

    def __init__(self, name, string, modifier):
        self.name = name
        self.string = string
        self.modifier = modifier

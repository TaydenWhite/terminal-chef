from Data.Items.Plate import Plate
from Rooms.Pantry import Pantry
from Rooms.Plating import Plating
from Data.Customer import Customer


class Game_Data:
    def __init__(self):
        self.play = True # game in progress
        
        self.curr_room = 0
        self.room_state = 0 
        
        self.end_time = 0

        self.trash_meter = 0
        self.money = 0
        self.inventory = [None, None, None]
        
        self.customers = [Customer(Plate(['Bread', 'Beef'], [], ['Potato'], 0, 'order', 'False'), 13), # Burger & Fries
                          Customer(Plate(['Bread', 'Beef'], ['Lettuce', 'Tomato'], [], 0, 'order', 'False'), 10), # Burger w/ Lettuce, Tomato
                          Customer(Plate(['Tomato'], [], ['Lettuce'], 0, 'order', 'False'), 8)] # Tomato Soup & Salad
        self.rooms = [Pantry(), Plating()]
        #      5
        #      4
        #   2     3
        #   0     1

    



#                      STATUS CHECK
#   //==============================================\\
#   ||   IN: SERVICE ROOM   ||     TRASH LVL: 8     ||
#   ||==============================================||
#   || OUTSTANDING ORDERS:                          ||
#   ||      1. Burger w/ Tomato, Lettuce && Fries   ||
#   ||      2. Potato Soup && Tomato Soup           ||
#   ||      3. Salad w/ Tomato                      ||
#   ||==============================================||
#   || CURRENT PROCESSES:                           ||
#   ||      1. PAN #1 [Beef]       5 SEC REMAINING  ||
#   ||      2. DISH WASHER        10 SEC REMAINING  ||
#   ||      3. CUSTOMER #3         3 SEC REMAINING  ||
#   ||==============================================||
#   || INVENTORY:                                   ||
#   ||      1.                                      ||
#   ||      2. [RTP] Beef                           ||
#   ||      3. [UNCUT] [UNCOOKED] Tomato            ||
#   ||==============================================||
#   || WARNINGS:                                    ||
#   ||      1. PAN #2 [POTATO]     5 SEC REMAINING  ||
#   ||      2. TRASH LEVEL             2 REMAINING  ||
#   \\==============================================//

    def status_menu(self):
        # get and print outstanding orders
        max = -10000
        order_strings = []
        for num, customer in enumerate(self.customers):
            if customer.get_state() == 0:
                string = f'{num + 1}. {str(customer.get_order)}'
                if len(string) > max: max = len(string)
                order_strings.append(string)

        # get current processes


        #get inventory




        print
        # NEED: curr_room, trash_lvl, 
        # customers.orders
        # curr_processes
        # inventory
        # warnings


        pass

    def room_menu(self):
        pass

    def action_menu(self):
        pass

    def inventory_menu(self):
        pass

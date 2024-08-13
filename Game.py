import Item
from Room import Pantry
from Room import Plating
import Customer

class Game:

    def __init__(self):
        self.play = True # game in progress
        self.curr_room = 0
        self.room_state = 0 
        self.end_time = 0

        self.trash_meter = 0
        self.money = 0
        self.inventory = [Item([], [], [], 0, True), Item([], [], [], 0, True), Item([], [], [], 0, True)]
        self.customers = [Customer(Item(['Bread', 'Beef'], [], ['Potato'], 0, 'order'), 13), # Burger & Fries
                          Customer(Item(['Bread', 'Beef'], ['Lettuce', 'Tomato'], [], 0, 'order'), 10), # Burger w/ Lettuce, Tomato
                          Customer(Item(['Tomato'], [], ['Lettuce'], 0, 'order'), 8)] # Tomato Soup & Salad
        self.rooms = [Pantry(), Plating()]
        #      5
        #      4
        #   2     3
        #   0     1



        self.curr_processes = [] # should be accessed through rooms -> actions -> countdowns

        def __str__(self):
            pass

    def set_end_time(self, end_time):
        self.end_time = end_time

    def get_end_time(self):
        return self.end_time

    def state_control(self, key):
        
        movements = ['Key.up', 'Key.down', 'Key.left', 'Key.right']
        selects = ['1', '2', '3', '4']
        exit = '5'
        
        if key in movements:
            self.move(key)
            self.room_state == 0
            self.room_menu()

        if key in selects:
            pass
            
            # (0, 0)
            # (0, 0)

        self.trash_meter += 1
        if self.trash_meter == 11:
            pass
            # PUNISHMENT


    def move(self, move):
        room = self.curr_room
        if move == 'Key.up':
            if room < 2:
                self.curr_room += 2
            elif room < 4:
                self.curr_room = 4
            elif room < 5:
                self.curr_room = 5
        elif move == 'Key.down':
            if room > 3:
                self.curr_room -= 1
            elif room > 1:
                self.curr_room -= 2
        elif move == 'Key.right':
            if room == 0 or room == 2:
                self.curr_room += 1
        else:
            if room == 1 or room == 3:
                self.curr_room -= 1



    def state_control(self, key):
        pass


    def status_menu(self):
        string = str((self.rooms)[self.curr_room], self)
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

class Game:

    def __init__(self, Rooms):
        self.play = True # game in progress
        self.curr_room = 0
        self.trash_meter = 0
        self.money = 0
        self.inventory = ['','','']
        self.room_state = 0 
        self.rooms = Rooms
        self.curr_processes = [] # should be accessed through rooms -> actions -> countdowns

        def __str__(self):
            pass


    def state_control(self, key):
        
        movements = ['Key.up', 'Key.down', 'Key.left', 'Key.right']
        selects = ['1', '2', '3', '4']
        exit = '5'
        
        if key in movements:
            self.move(key)
            self.room_state == 0

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
        if key in 


    def status_menu(self):
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

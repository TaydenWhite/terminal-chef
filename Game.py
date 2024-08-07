class Game:

    def __init__(self, Rooms):
        self.play = True # game in progress
        self.curr_room = 0
        self.trash_meter = 0
        self.money = 0
        self.inventory = ['','','']
        self.player_state = 0 
            # 0 - in room | next input selects action
            # 1 - in action | next input selects inventory slot
            # 2 - Action selected | 
        self.rooms = Rooms

    def game_inputs(self, key):
        
        movements = ['Key.up', 'Key.down', 'Key.left', 'Key.right']
        selects = ['1', '2', '3', '4']
        exit = '5'

        
        if key in movements:
            self.move(key)

        if key in selects:
            
            # (0, 0)
            # (0, 0)



        
        if key == exit:
            print(self)


    def __str__(self):
        pass

        # dictionary

        # ROOM



    def menus(self, key):
        (self.rooms[self.curr_room]).menu(self)


        

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

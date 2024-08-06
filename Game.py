class Game:

    def __init__(self):
        self.play = True # game in progress
        self.curr_room = 0
        self.trash_meter = 0
        self.money = 0
        self.inventory = ["","",""]
        self.player_state = 0 
            # 0 - in room | next input selects action
            # 1 - in action | next input selects inventory slot
            # 2 - Action selected | 
        #self.rooms = Rooms

    def game_inputs(self, key):
        
        movements = ['Key.up', 'Key.down', 'Key.left', 'Key.right']
        selects = ['1', '2', '3']
        status = '4'

        
        if key in movements:
            self.move(key)

        if key in selects:
            pass
        
        if key == status:
            print(self)


    def __str__(self):
        pass

#                      STATUS CHECK
#   //==============================================\\
#   ||   IN: SERVICE ROOM   ||     TRASH LVL: 8     ||
#   ||==============================================||
#   || OUTSTANDING ORDERS:                          ||
#   ||      1. Burger w/ Tomato & Lettuce           ||
#   ||      2. Potato Soup && Tomato Soup           ||
#   ||      3. Salad w/ Tomato                      ||
#   ||==============================================||
#   || CURRENT PROCESSES:                           ||
#   ||      1. BEEF ON PAN #1      5 SEC REMAINING  ||
#   ||      2. DISH WASHER        10 SEC REMAINING  ||
#   ||      3. CUSTOMER #3         3 SEC REMAINING  ||
#   ||==============================================||
#   || INVENTORY:                                   ||
#   ||      1.                                      ||
#   ||      2. [RTP] Beef                           ||
#   ||      3. [UNCUT] [UNCOOKED] Tomato            ||
#   ||==============================================||
#   || WARNINGS:                                    ||
#   ||      1. POTATO IN PAN #2    5 SEC REMAINING  ||
#   ||      2. TRASH LEVEL             2 REMAINING  ||
#   \\==============================================//
#
#
# [UNCOOKED] Beef
# [UNCUT] [UNCOOKED] Tomato




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

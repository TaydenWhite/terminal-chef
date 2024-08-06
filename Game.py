class Game:

    def __init__(self):
        self.play = True # game in progress
        self.curr_room = 0
        self.trash_meter = 0
        self.money = 0
        self.inventory = ["","",""]
        #self.rooms = Rooms

    def move(self, move):
        if move == 'Key.up':
            if self.curr_room < 2:
                self.curr_room += 2
            elif self.curr_room == 2 or self.curr_room == 3:
                self.curr_room == 4
            elif self.curr_room == 4:
                self.curr_room += 1

        elif move == 'Key.down':
            if self.curr_room > 3:
                self.curr_room -= 1
            elif self.curr_room > 1:
                self.curr_room -= 2
        elif move == 'Key.right':
            if self.curr_room == 0 or self.curr_room == 2:
                self.curr_room += 1
        elif move == 'Key.left':
            if self.curr_room == 1 or self.curr_room == 3:
                self.curr_room -= 1
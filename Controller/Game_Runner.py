import sys
import os

# Add the base directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Data.Game_Data import Game_Data
from Visuals import Game_Draw

class Game_Runner:
    def __init__(self, game_data: Game_Data, game_draw: Game_Draw):
        self.game_data = game_data # data object
        self.game_draw = game_draw # draw object

    def state_control(self, key):
        
        print(f'{key}')

        #movements = ['Key.up', 'Key.down', 'Key.left', 'Key.right']
        #selects = ['1', '2', '3', '4']
        #exit = '5'
        
        #if key in movements:
        #    self.move(key)
        #    self.room_state == 0
        #    self.room_menu()

        #if key in selects:
        #    pass
            
            # (0, 0)
            # (0, 0)

        #self.trash_meter += 1
        #if self.trash_meter == 11:
        #    pass
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
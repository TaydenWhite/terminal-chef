import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
from Data.Items.Plate import Plate

class Cleaning:

    def __init__(self):
        self.dish_washer = False
        self.dish_washer_item = 0
        self.dish_end = datetime.now()
        
        self.trash_disposal = False
        self.trash_end = datetime.now()

    def start_washer(self, plate: Plate):
        self.dish_washer = True
        self.dish_washer_item = plate
        self.dish_end = datetime.now() + timedelta(seconds = 10)

    def start_trash_disposal(self):
        self.trash_disposal = True
        self.trash_end = datetime.now() + timedelta(seconds = 10)


    def get_dish_remaining(self):
        diff = (self.dish_end - datetime.now()).total_seconds()
        if diff < 0: 
            self.dish_washer = False
            self.dish_washer_item = 0
            return 0
        
        return round(diff)
    
    def get_dish_remaining(self):
        diff = (self.trash_end - datetime.now()).total_seconds()
        if diff < 0: 
            self.trash_disposal = False
            return 0
        
        return round(diff)


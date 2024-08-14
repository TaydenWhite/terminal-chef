from datetime import datetime, timedelta

class Cleaning:

    def __init__(self):
        self.dish_washer = False
        self.dish_end = datetime.now()
        
        
        self.trash_disposal = False
        self.trash_end = datetime.now()

from Data.Items.Plate import Plate

class Plating():
    def __init__(self):
        self.plates = [Plate([], [], [], 1, True),
                       Plate([], [], [], 2, True),
                       Plate([], [], [], 3, True)]
        
    def get_plates(self): return self.plates
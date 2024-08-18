import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
from Data.Items.Ingredient import Ingredient 

class Stoves:
    def __init__(self):
        self.pan1 = False
        self.pan1_ingredient = Ingredient('', {}, False)
        self.pan1_end = datetime.now()

        self.pan2 = False
        self.pan2_ingredient = Ingredient('', {}, False)
        self.pan2_end = datetime.now()

        self.pot1 = False
        self.pot1_ingredient = Ingredient('', {}, False)
        self.pot1_end = datetime.now()

        self.pot2 = False
        self.pot2_ingredient = Ingredient('', {}, False)
        self.pot2_end = datetime.now()

    def start_pan1(self, ingredient: Ingredient):
        self.pan1 = True
        self.pan1_end = datetime.now() + timedelta(seconds = 10)
        self.pan1_ingredient = ingredient          
        
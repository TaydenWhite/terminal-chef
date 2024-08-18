import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Data.Items.Ingredient import Ingredient

class Prep():
    def __init__(self):
        pass

    def wash_ingredient(self, ingredient: Ingredient):
        ingredient.swap_tag('[UNWASHED]')

    def cut_ingredient(self, ingredient: Ingredient):
        ingredient.swap_tag('[UNCUT]')

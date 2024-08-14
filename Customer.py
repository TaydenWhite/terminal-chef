from enum import Enum

class State(Enum):
    WAITING = 0
    EATING = 1
    DONE = 2


class Customer:

    def __init__(self, order, price):
        self.order = order # order is a 
        self.price = price
        self.state = State.WAITING
        
    def get_order(self):
        return self.order
    
    def get_price(self):
        return self.price
    
    def get_state(self):
        return self.state
    
    def set_order(self, order):
        self.order = order

    def set_price(self, price):
        self.price = price

    def set_state(self, state):
        self.state = state
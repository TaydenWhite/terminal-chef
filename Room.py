class Room:

    def __init__(self, name):
        self.name = name


    def __str__(self):
        pass


class Action:

    def __init__(self, name, string, modifier):
        self.name = name
        self.string = string
        self.modifier = modifier

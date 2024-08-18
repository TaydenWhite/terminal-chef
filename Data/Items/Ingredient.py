class Ingredient:
    def __init__(self, name, tags, show_tags):
        self.name = name
        self.tags = tags
        self.show_tags = show_tags # only show tags in inventory 

        # example tags input
        # tags = {'[RTP]' : False, '[UNWASHED]' : True, 
        #        '[UNCUT]' : False, '[UNCOOKED]' : True, '[BURNED]' : False}

    def __str__(self):
        string = ''
        
        if self.show_tags:
            for tag in self.tags:
                if self.tags[tag]: string += f'{tag} '
        string += self.name

        return string

    # ingredients are: Tomato, Potato, Lettuce, Beef, Chicken, Bread

    def get_name(self): return self.name
    def get_tags(self): return self.tags

    def swap_tag(self, tag): self.tags[tag] = not self.tags[tag]
class Entity:
    '''
    A generic object to represent players, enemies, items, etc
    Holds the x and y coordinates, character [symbol], and color
    '''
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # move the entity by a given amount
        self.x += dx
        self.y += dy
class Entity:
    """
    A generic object to represent players, enemies, items, etc
    Holds the x and y coordinates, character [symbol], and color
    """
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        # move the entity by a given amount
        self.x += dx
        self.y += dy


# loop through entities - if one is blocking and is at the x/y location specified, return it
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None

from map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):

        # initialize a 2D aray of tiles, set to blocking by default
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    # creates a room that can be explored by the player
    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        # the + 1 is necessary in order to form walls between rectangles that could be next to each other
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

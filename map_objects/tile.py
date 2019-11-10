class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # by default, if a tile is blocked, it also blocks sight
        # this way, don't need to pass block_sight every time, it can be assumed to be the same as blocked
        # by separating them, can have a see-through tile which cannot be crossed, or vice-versa
        if block_sight is None:
            block_sight = blocked;

        self.block_sight = block_sight

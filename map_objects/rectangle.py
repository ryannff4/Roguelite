'''
Helper class for dungeon rooms. Holds info about dimensions, which will be known as Rect (rectangles)
'''
class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
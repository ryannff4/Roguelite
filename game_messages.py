import tcod as libtcod

import textwrap


# store the message text and the color to draw it with (white is default color)
class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color


# holds a list of messages, its x coordinate, and width/height. Width/height are useful to help know when to cut off the top messages
class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # if the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))
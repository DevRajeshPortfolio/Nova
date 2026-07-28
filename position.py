# position.py
class Position:
    def __init__(self, index, line, column, filename):
        self.index = index
        self.line = line
        self.column = column
        self.filename = filename

    def advance(self, current_char=None):
        """Advance position by one character"""
        self.index += 1
        self.column += 1

        if current_char == '\n':
            self.line += 1
            self.column = 0

        return self

    def copy(self):
        """Create a copy of this position"""
        return Position(self.index, self.line, self.column, self.filename)
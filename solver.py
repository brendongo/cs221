import string

class Solver:
    def __init__(self):
        self.todo = 0

    def decrypt(self, text):
        return (text, string.ascii_uppercase)
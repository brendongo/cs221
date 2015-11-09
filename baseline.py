import util, string

class Baseline:
    def __init__(self):
        self.todo = 0

    def decrypt(self, text):
        # TODO decrypt using letter frequencies
        # guess = util.encrypt(text, string.ascii_uppercase, letter_frequency_key)
        return (text, string.ascii_uppercase)
import util, string

class Baseline:
    '''
    Baseline generates a key for the cipher_text based on charaacter freuencies.

    It counts the character frequencies of the cipher text and makes a key so that the 
    most common letter in the cipher text maps to the most common letter in english, E, the 
    second most common letter maps to the next most common letter in english, T, etc.

    We got the data for letter frequencies from http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html

    It could have also been done manually on the training data but we would get similar results.
    '''
    
    def __init__(self):
        self.todo = 0
        # From http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
        self.charFreq = {"E":12.02,"T":9.10,"A":8.12,"O":7.68,"I":7.31,"N":6.95,"S":6.28,"R":6.02,"H":5.92,"D":4.32,"L":3.98,"U":2.88,"C":2.71,"M":2.61,"F":2.30,"Y":2.11,"W":2.09,"G":2.03,"P":1.82,"B":1.49,"V":1.11,"K":0.69,"X":0.17,"Q":0.11,"J":0.10,"Z":0.07}
        self.letters_by_freq = "".join(sorted(self.charFreq, key=self.charFreq.get, reverse=True))

    def decrypt(self, text):
        # Count character frequencies of text
        cipher_char_frequency = {}
        for i in string.ascii_uppercase:
            cipher_char_frequency[i] = 0

        for i in text:
            if i in string.ascii_letters:
                cipher_char_frequency[i.upper()] = cipher_char_frequency.get(i.upper()) + 1

        cipher_letters_by_freq = "".join(sorted(cipher_char_frequency, key=cipher_char_frequency.get, reverse=True))
        key = util.encrypt(string.ascii_uppercase, cipher_letters_by_freq, self.letters_by_freq)
        return (key, util.encrypt(text, string.ascii_uppercase, key))

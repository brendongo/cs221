import util, string

class Baseline:
    def __init__(self):
        self.todo = 0
        self.charFreq = {"E":12.02,"T":9.10,"A":8.12,"O":7.68,"I":7.31,"N":6.95,"S":6.28,"R":6.02,"H":5.92,"D":4.32,"L":3.98,"U":2.88,"C":2.71,"M":2.61,"F":2.30,"Y":2.11,"W":2.09,"G":2.03,"P":1.82,"B":1.49,"V":1.11,"K":0.69,"X":0.17,"Q":0.11,"J":0.10,"Z":0.07}
        self.letters_by_freq = "".join(sorted(self.charFreq, key=self.charFreq.get, reverse=True))

    def decrypt(self, text):
        print text
        # Count character frequencies of text
        cipher_char_frequency = {}
        for i in string.ascii_uppercase:
            cipher_char_frequency[i] = 0

        for i in text:
            if i in string.ascii_letters:
                cipher_char_frequency[i.upper()] = cipher_char_frequency.get(i.upper()) + 1
        cipher_letters_by_freq = "".join(sorted(cipher_char_frequency, key=cipher_char_frequency.get, reverse=True))


        key = util.encrypt(string.ascii_uppercase, cipher_letters_by_freq, self.letters_by_freq)

        print self.letters_by_freq
        print cipher_letters_by_freq
        print key
        print util.encrypt(text, string.ascii_uppercase, key)
        return (key, util.encrypt(text, string.ascii_uppercase, key))

from copy import copy,deepcopy
from collections import Counter
import util
import math
import string
import LanguageModel
import random
import operator

class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.iteritems())))

class Solver:
    def __init__(self):
        self.todo = 0
        self.languagemodel = LanguageModel.LanguageModel('test')
        # From http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
        self.charFreq = {"E":12.02,"T":9.10,"A":8.12,"O":7.68,"I":7.31,"N":6.95,"S":6.28,"R":6.02,"H":5.92,"D":4.32,"L":3.98,"U":2.88,"C":2.71,"M":2.61,"F":2.30,"Y":2.11,"W":2.09,"G":2.03,"P":1.82,"B":1.49,"V":1.11,"K":0.69,"X":0.17,"Q":0.11,"J":0.10,"Z":0.07}

    def decrypt(self, cipherText):

        def swapIndices(a, b, key):
            tempKey = list(key)
            tempKey[a], tempKey[b] = tempKey[b], tempKey[a]
            return "".join(tempKey)

        def sample(swaps):
            r = random.random()
            start = 0
            for swap in swaps:
                start += swap[0]
                if r <= start: return swap

        key = util.generateKey()
        for i in xrange(100000):
            for a in xrange(len(key)):
                swaps = []
                for b in xrange(len(key)):
                    temp_key = swapIndices(a, b, key)
                    temp_score = self.languagemodel.score(util.encrypt(cipherText, string.ascii_uppercase, temp_key))
                    swaps.append((temp_score, temp_key))

                # convert to probabilities
                maxSwap = max(swaps, key=operator.itemgetter(0))
                swaps = [(math.e ** (swap[0] - maxSwap[0]),swap[1]) for swap in swaps]
                scoreSum = sum([swap[0] for swap in swaps])
                swaps = [(float(swap[0])/scoreSum,swap[1]) for swap in swaps]

                # sample randomly
                key = sample(swaps)[1]

            print i, key, util.encrypt(cipherText, string.ascii_uppercase, key)

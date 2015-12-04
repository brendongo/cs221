from copy import copy,deepcopy
from collections import Counter
import util
import math
import string
import LanguageModel
import random

class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.iteritems())))

class SubstitutionProblem(util.SearchProblem):

    def __init__(self, cipherText, cipherFreqMap, dictFreqMap):
        self.cipherText = cipherText
        self.cipherFreqMap = cipherFreqMap
        self.dictFreqMap = dictFreqMap

    def nextCharToMap(self, state):
        mappedChars = state.keys()
        for c in list(self.cipherText.upper()):
            if c not in mappedChars and ord(c) < 91 and ord(c) >= 65: return c

    def startState(self): return HashableDict()

    def isGoal(self, state): return len(state) == 12

    def succAndCost(self, state):
        succ = []
        cipherChar = self.nextCharToMap(state)
        availableChars = set()
        for i in xrange(65, 91): availableChars.add(chr(i))
        availableChars -= set(state.values())
        for c in availableChars:
            newState = deepcopy(state)
            newState[cipherChar] = c
            # error margin
            # weight = abs(self.cipherFreqMap[cipherChar] - self.dictFreqMap[c])/self.dictFreqMap[c]
            # quotient
            # weight = abs(self.cipherFreqMap[cipherChar] / self.dictFreqMap[c])
            # difference
            weight = abs(self.cipherFreqMap[cipherChar] - self.dictFreqMap[c])
            succ.append(((cipherChar,c), newState, weight))

        return succ


class Solver:
    def __init__(self):
        self.todo = 0
        self.languagemodel = LanguageModel.LanguageModel('test')
        # From http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
        self.charFreq = {"E":12.02,"T":9.10,"A":8.12,"O":7.68,"I":7.31,"N":6.95,"S":6.28,"R":6.02,"H":5.92,"D":4.32,"L":3.98,"U":2.88,"C":2.71,"M":2.61,"F":2.30,"Y":2.11,"W":2.09,"G":2.03,"P":1.82,"B":1.49,"V":1.11,"K":0.69,"X":0.17,"Q":0.11,"J":0.10,"Z":0.07}

    def decrypt(self, cipherText):
        def swap(key):
            key = list(key)
            x = random.randrange(0,len(key))
            y = random.randrange(0,len(key))
            key[x], key[y] = key[y], key[x]
            return "".join(key)

        best_cipher_key = util.generateKey()
        best_score = self.languagemodel.score(util.encrypt(cipherText, string.ascii_uppercase, best_cipher_key))
        curr_cipher_key = best_cipher_key
        curr_score = best_score
        for i in xrange(2000):
            temp = swap(curr_cipher_key)
            temp_score = self.languagemodel.score(util.encrypt(cipherText, string.ascii_uppercase, temp))
            if temp_score > curr_score:
              curr_cipher_key = temp
              curr_score = temp_score

              if temp_score > best_score:
                best_cipher_key = temp
                best_score = temp_score
                # print best_score, i, util.encrypt(cipherText, string.ascii_uppercase, temp)

            # elif random.random() * best_score < temp_score:
            #   curr_cipher_key = temp
            #   curr_score = temp_score

        return (util.encrypt(cipherText, string.ascii_uppercase, best_cipher_key), best_cipher_key)

        # for k in self.charFreq: self.charFreq[k] /= 100.0

        # cipherFreqMap = Counter()
        # for c in list(cipherText.upper()): cipherFreqMap[c] += 1
        # for c in cipherFreqMap.keys():
        #     if ord(c) >= 91 or ord(c) < 65: del cipherFreqMap[c]
        # total = sum(cipherFreqMap.values(), 0.0)
        # for c in cipherFreqMap.keys(): cipherFreqMap[c] = cipherFreqMap[c] / total

        # ucs = util.UniformCostSearch(verbose=0)
        # ucs.solve(SubstitutionProblem(cipherText, cipherFreqMap, self.charFreq))

        # print ucs.actions

        # mapping = {}
        # for a in ucs.actions: mapping[a[1]] = a[0]
        # key = ""
        # for i in xrange(65,91):
        #     if chr(i) in mapping: key += mapping[chr(i)]
        #     else: key += "?"

        # print key
        # decryptedText = util.encrypt(cipherText, string.ascii_uppercase, key)
        # print decryptedText
        # return (decryptedText, key)

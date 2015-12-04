from copy import copy,deepcopy
from collections import Counter
import util
import math
import string
import LanguageModel
import random
import operator
import sys

class Solver:
  def __init__(self, languagemodel):
    self.todo = 0
    self.languagemodel = languagemodel

  def decrypt(self, cipherText):
    upperCipher = cipherText.upper()
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

    def gibbs(key):
      best_swap = (float('-inf'),"")
      for i in xrange(200):
        last_n = []
        for a in xrange(len(key)):
          swaps = []
          for b in xrange(len(key)):
            temp_key = swapIndices(a, b, key)
            temp_score = self.languagemodel.score(util.encrypt(upperCipher, temp_key))
            temp_swap = (temp_score, temp_key)
            if temp_swap[0] > best_swap[0]: best_swap = temp_swap
            swaps.append(temp_swap)

          # convert to probabilities
          maxSwap = max(swaps, key=operator.itemgetter(0))
          swaps = [(math.e ** (swap[0] - maxSwap[0]),swap[1],swap[0]) for swap in swaps]
          scoreSum = sum([swap[0] for swap in swaps])
          swaps = [(float(swap[0])/scoreSum,swap[1],swap[2]) for swap in swaps]

          # sample randomly
          selected = sample(swaps)
          key = selected[1]

          # keep last n swaps
          last_n.append(selected)
          last_n = last_n[-10:]

          # check for convergence
          if sum([abs((swap[2] - best_swap[0])/best_swap[0]) == 0 for swap in last_n]) == 10:
            return best_swap

        decrypted = util.encrypt(upperCipher, best_swap[1])
        sys.stdout.write('.')
        sys.stdout.flush()

      return best_swap

    best_swap = (float('-inf'),"")
    for i in xrange(10):
      key = util.generateKey()
      swap = gibbs(key)
      if swap[0] > best_swap[0]: best_swap = swap

      sys.stdout.write(str(float(i+1)/10 * 100) + "%")
      sys.stdout.flush()

    translated = util.encryptCase(cipherText, best_swap[1])
    print "\nBEST: ", best_swap[0], translated
    return translated, best_swap[1]

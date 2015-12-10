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
    self.numIters = 10

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
      last_n = []
      for i in xrange(200):
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
        converge_n = 5
        last_n.append(best_swap)
        last_n = last_n[-converge_n:]

        # print best_swap[0], util.encrypt(upperCipher, best_swap[1])

        # check for convergence
        avgSwap = sum([swap[0] for swap in last_n]) / float(converge_n)
        if sum([abs(swap[0] - avgSwap) <= 1 for swap in last_n]) == converge_n:
          return best_swap

        decrypted = util.encrypt(upperCipher, best_swap[1])
        sys.stdout.write('.')
        sys.stdout.flush()

      return best_swap

    best_swap = (float('-inf'),"")
    num_best = 0
    for i in xrange(self.numIters):
      key = util.generateKey()
      swap = gibbs(key)
      if swap[0] == best_swap[0]: num_best += 1
      if swap[0] > best_swap[0]:
        best_swap = swap
        num_best = 1

      sys.stdout.write(str(float(i+1)/self.numIters * 100) + "%")
      sys.stdout.flush()

    translated = util.encryptCase(cipherText, best_swap[1])
    print "\n", num_best, "BEST: ", best_swap[0], translated
    return translated, best_swap[1], num_best

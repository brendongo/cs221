import math, collections, string

class LanguageModel:

  def __init__(self, corpus):
    self.trigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.characterBigramCounts = collections.defaultdict(lambda: 0)
    self.characterTrigramCounts = collections.defaultdict(lambda: 0)
    self.characterUnigramCounts = collections.defaultdict(lambda: 0)
    self.train(corpus)

  def train(self, corpus):
    '''Train Language Model on Corpus'''
    nGramsFile = open(corpus, 'r')
    for line in nGramsFile: # split into words first
      line = " " + line + " "
      lineLen = len(line)
      for i in xrange(0, lineLen - 2):
        self.characterUnigramCounts[line[i].lower()] += 1
        self.characterBigramCounts[line[i:i+2].lower()] += 1
        self.characterTrigramCounts[line[i:i+3].lower()] += 1
      self.characterBigramCounts[line[lineLen-2:lineLen].lower()] += 1
      self.characterUnigramCounts[line[lineLen-2].lower()] += 1

      sentence = line.split()
      sentenceLen = len(sentence)
      for i in xrange(0, sentenceLen - 2):
        first = sentence[i]
        second = sentence[i+1]
        third = sentence[i+2]

        self.trigramCounts[(first, second, third)] += 1
        self.bigramCounts[(first, second)] += 1
        self.unigramCounts[first] += 1

    for char in self.characterUnigramCounts:
      self.characterUnigramCounts[char] = math.log(self.characterUnigramCounts[char])
    for bigram in self.characterBigramCounts:
      self.characterBigramCounts[bigram] = math.log(self.characterBigramCounts[bigram])
    for trigram in self.characterTrigramCounts:
      self.characterTrigramCounts[trigram] = math.log(self.characterTrigramCounts[trigram])
    for word in self.unigramCounts:
      self.unigramCounts[word] = math.log(self.unigramCounts[word])
    for bigram in self.bigramCounts:
      self.bigramCounts[bigram] = math.log(self.bigramCounts[bigram])
    for trigram in self.trigramCounts:
      self.trigramCounts[trigram] = math.log(self.trigramCounts[trigram])

  def score(self, sentence):
    # sentence is a string
    words = sentence.split()

    characterScore = 1.0
    wordScore = 1.0

    for i, word in enumerate(words):
      wordScore += self.unigramCounts[word]

      length = len(word)

      for j in xrange(length):
        characterScore += self.characterUnigramCounts[word[j]]

      word = " " + word + " "

      for j in xrange(length - 1):
        characterScore += self.characterBigramCounts[word[j:j+2]]

      for j in xrange(length - 2):
        characterScore += self.characterTrigramCounts[word[j:j+3]]

    return characterScore + wordScore

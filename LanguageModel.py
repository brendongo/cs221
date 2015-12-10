import math, collections, string

class LanguageModel:

  def __init__(self, corpus):
    self.trigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.characterBigramCounts = collections.defaultdict(lambda: 0)
    self.characterTrigramCounts = collections.defaultdict(lambda: 0)
    self.characterUnigramCounts = collections.defaultdict(lambda: 0)
    self.wildcardWords = collections.defaultdict(lambda: {})
    self.train(corpus)

  def addToWildcardWords(self, word):
    chars = list(word)
    for i in xrange(len(word)):
      chars[i] = '_'
      self.wildcardWords[''.join(chars)] = word
      chars[i] = word[i]

  def train(self, corpus):
    '''Train Language Model on Corpus'''
    nGramsFile = open(corpus, 'r')
    for line in nGramsFile: # split into words first
      line = " " + line + " "
      line = line.upper()
      lineLen = len(line)
      for i in xrange(0, lineLen - 2):
        self.characterUnigramCounts[line[i]] += 1
        self.characterBigramCounts[line[i:i+2]] += 1
        self.characterTrigramCounts[line[i:i+3]] += 1
      self.characterBigramCounts[line[lineLen-2:lineLen]] += 1
      self.characterUnigramCounts[line[lineLen-2]] += 1

      sentence = line.split()
      sentenceLen = len(sentence)
      for i in xrange(0, sentenceLen - 2):
        first = sentence[i]
        second = sentence[i+1]
        third = sentence[i+2]

        self.addToWildcardWords(first)

        self.trigramCounts[(first, second, third)] += 1
        self.bigramCounts[(first, second)] += 1
        self.unigramCounts[first] += 1

      if len(sentence) >= 1: self.addToWildcardWords(sentence[-1])
      if len(sentence) >= 2: self.addToWildcardWords(sentence[-2])

    for key in self.wildcardWords:
      if self.wildcardWords[key] == 'ADVENTURE': print key

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
      if i < len(words) - 1: 
        wordScore += self.bigramCounts[(word, words[i+1])]

      length = len(word)

      for j in xrange(length):
        characterScore += self.characterUnigramCounts[word[j]]

      word = " " + word + " "

      for j in xrange(length - 1):
        characterScore += self.characterBigramCounts[word[j:j+2]]

      for j in xrange(length - 2):
        characterScore += self.characterTrigramCounts[word[j:j+3]]

    # print characterScore, wordScore
    return characterScore + wordScore * 10

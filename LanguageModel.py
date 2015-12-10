import math, collections, string, operator

class LanguageModel:

  def __init__(self, corpus):
    self.trigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.characterBigramCounts = collections.defaultdict(lambda: 0)
    self.characterTrigramCounts = collections.defaultdict(lambda: 0)
    self.characterUnigramCounts = collections.defaultdict(lambda: 0)
    self.wildcardWords = collections.defaultdict(lambda: set())
    self.KWildcards = 10
    self.train(corpus)

  def addToWildcardWords(self, word):
    chars = list(word)
    for i in xrange(len(word)):
      chars[i] = '_'
      self.wildcardWords[''.join(chars)].add((word, 1))
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
    wordScore = 0
    characterScore = 0
    bestPossibleSentences = [([], 0)]

    for i, word in enumerate(words):
      wordScore += self.unigramCounts[word]

      # if i < len(words) - 1: 
      #   wordScore += self.bigramCounts[(word, words[i+1])]      

      possibleCompletions = set()
      chars = list(word)
      for i in xrange(len(word)):
        chars[i] = '_'
        possibleCompletions |= self.wildcardWords[''.join(chars)]
        chars[i] = word[i]
      
      partialSentences = []
      for sentence in bestPossibleSentences:
        if len(possibleCompletions) == 0: partialSentences.append((sentence[0] + [''], sentence[1]))
        for completion in possibleCompletions:
          realWord = completion[0]
          distanceWeight = 1 if realWord == word else .3
          score = 0 if len(sentence[0]) < 1 else sentence[1] + self.bigramCounts[(sentence[0][-1], realWord)] * distanceWeight
          partialSentences.append((sentence[0] + [realWord], score))

      partialSentences = sorted(partialSentences, key=operator.itemgetter(1), reverse=True)
      bestPossibleSentences = partialSentences[:self.KWildcards]

      length = len(word)
      for j in xrange(length):
        characterScore += self.characterUnigramCounts[word[j]]

      word = " " + word + " "

      for j in xrange(length - 1):
        characterScore += self.characterBigramCounts[word[j:j+2]]

      for j in xrange(length - 2):
        characterScore += self.characterTrigramCounts[word[j:j+3]]

    maxSentence = max([([], 0)] + bestPossibleSentences, key=operator.itemgetter(1))
    print maxSentence[0]
    sentenceScore = maxSentence[1]

    return characterScore + wordScore + sentenceScore * 10

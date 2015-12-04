import math, collections

class LanguageModel:

  def __init__(self, corpus):
    self.trigramCounts = collections.defaultdict(lambda: 0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.characterBigramCounts = collections.defaultdict(lambda: 0)
    self.characterTrigramCounts = collections.defaultdict(lambda: 0)
    self.characterUnigramCounts = collections.defaultdict(lambda: 0)
    self.unigramtotal = 0
    self.bigramtotal = 0
    self.trigramtotal = 0
    self.characterUnigramTotal = 0
    self.train(corpus)

  def train(self, corpus):
    '''Train Language Model on Corpus'''
    nGramsFile = open(corpus, 'r')
    for line in nGramsFile:
      for j in xrange(0, len(line) - 2):
        char1 = line[j]
        char2 = line[j+1]
        char3 = line[j+2]

        charBigram = char1 + '&' + char2
        charTrigram = char1 + '&' + char2 + '&' + char3
        self.characterBigramCounts[charBigram] += 1
        self.characterTrigramCounts[charTrigram] += 1
        self.characterUnigramCounts[char1] += 1
        self.characterUnigramTotal += 1

      sentence = line.split()
      for i in xrange(0, len(sentence) - 2):
        first = sentence[i]
        second = sentence[i+1]
        third = sentence[i+2]

        trigram = first + "&" + second + "&" + third
        self.trigramCounts[trigram] += 1
        self.trigramtotal += 1

        bigram = first + "&" + second
        self.bigramCounts[bigram] += 1
        self.bigramtotal += 1

        self.unigramCounts[first] += 1
        self.unigramtotal += 1


    # Code below to initialize with ngrams file with format count word word word in each line
    # nGramsFile = open(corpus, 'r')
    # for line in nGramsFile:
    #   count, first, second, third = line.split()
    #   count = int(count)

    #   trigram = first + "&" + second + "&" + third
    #   self.trigramCounts[trigram] += count

    #   bigram = first + "&" + second
    #   self.bigramCounts[bigram] += count
    #   bigram = second + "&" + third
    #   self.bigramCounts[bigram] += count

    #   self.unigramCounts[first] += count
    #   self.unigramCounts[second] += count
    #   self.unigramCounts[third] += count
    #   self.unigramtotal += 3*count

  def score(self, sentence):
    # sentence is a string
    sentence = " " + sentence + " "

    characterScore = 1.0
    for word in sentence.split():
      for i in xrange(len(word)):
        unigramcount = self.characterUnigramCounts[word[i]]
        unigramScore = math.log(float(unigramcount + 1))
        characterScore += unigramScore

    #  for i in xrange(len(word) - 1):
     #   bigramcount = self.characterBigramCounts[word[i] + "&" + word[i + 1]]
      #  bigramScore = math.log(float(bigramcount + 1))
       # characterScore += bigramScore

      for i in xrange(len(word) - 2):
        trigramcount = self.characterTrigramCounts[word[i] + "&" + word[i + 1] + "&" + word[i + 2]]
        trigramScore = math.log(float(trigramcount + 1))
        characterScore += trigramScore

    #return characterScore

    # Character Score
    for i in xrange(0, len(sentence) - 2):
      first = sentence[i]
      second = sentence[i + 1]
      #third = sentence[i + 2]

      #trigram = first + "&" + second + "&" + third
      #trigramcount = self.characterTrigramCounts[trigram]

      bigram = first + "&" + second
      bigramcount = self.characterBigramCounts[bigram]

      bigramScore = math.log(float(bigramcount + 1)) #- math.log(len(sentence) + 26 ** 2)
      #trigramScore = math.log(float(trigramcount + 1)) - math.log(len(sentence) + 26 ** 3)
      characterScore += bigramScore


    # wordScore = 0.0
    # sentence = sentence.split()
    # for i in xrange(0,len(sentence) - 2):
    #   first = sentence[i]
    #   second = sentence[i+1]
    #   third = sentence[i+2]

    #   trigram = first + "&" + second + "&" + third
    #   trigramcount = self.trigramCounts[trigram]

    #   bigram = first + "&" + second
    #   bigramcount = self.bigramCounts[bigram]

    #   trigramScore = 0.0
    #   if trigramcount > 0:
    #     #tri-gram
    #     trigramScore = float(trigramcount)/bigramcount
    #     # trigramScore += math.log(trigramcount)
        # trigramScore -= math.log(bigramcount)

      # Trigram works better without backing up
      # bigramScore = 0.0
      # if bigramcount > 0:
      #   #Bi-gram
      #   bigramScore += math.log(bigramcount)
      #   bigramScore -= math.log(self.unigramCounts[first])

      # unigramScore = 0.0
      # unigramScore += math.log(self.unigramCounts[second] + 1)
      # unigramScore -= math.log(self.unigramtotal + len(self.unigramCounts))

      # wordScore += trigramScore # + unigramScore + bigramScore;

    return characterScore

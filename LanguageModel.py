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
        self.characterUnigramCounts[line] += 1
        self.characterUnigramTotal += 1

      sentence = line.split()
      for i in xrange(0, len(sentence) - 2):
        first = sentence[i]
        second = sentence[i+1]
        third = sentence[i+2]

        trigram = first + "&" + second + "&" + third
        self.trigramCounts[trigram] += 1
        
        bigram = first + "&" + second
        self.bigramCounts[bigram] += 1
        
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
    
    characterScore = 1.0
    # Character Score
    for i in xrange(0, len(sentence) - 2):
      first = sentence[i]
      second = sentence[i + 1]
      third = sentence[i + 2]
      
      trigram = first + "&" + second + "&" + third
      trigramcount = self.characterTrigramCounts[trigram]

      bigram = first + "&" + second
      bigramcount = self.characterBigramCounts[bigram]
      
      trigramScore = float(trigramcount + 1)/(bigramcount + len(self.characterBigramCounts) + 1)     

      # trigramScore = 0.0
      # if trigramcount > 0:
      #   #tri-gram
      #   trigramScore = float(trigramcount)/bigramcount
        # trigramScore += math.log(trigramcount) 
        # trigramScore -= math.log(bigramcount)

      # Trigram works better without backing up
      # bigramScore = 0.0
      # if bigramcount > 0:  
      #   #Bi-gram
      #   bigramScore += math.log(bigramcount)
      #   bigramScore -= math.log(self.characterUnigramCounts[first])

      # unigramScore = 0.0      
      # unigramScore += math.log(self.characterUnigramCounts[second] + 1) 
      # unigramScore -= math.log(self.characterUnigramTotal + len(self.characterUnigramCounts))  

      characterScore += trigramScore # + unigramScore + bigramScore


    wordScore = 0.0 
    sentence = sentence.split()
    for i in xrange(0,len(sentence) - 2):
      first = sentence[i]
      second = sentence[i+1]
      third = sentence[i+2]
      
      trigram = first + "&" + second + "&" + third
      trigramcount = self.trigramCounts[trigram]

      bigram = first + "&" + second
      bigramcount = self.bigramCounts[bigram]
      
      trigramScore = 0.0
      if trigramcount > 0:
        #tri-gram
        trigramScore = float(trigramcount)/bigramcount
        # trigramScore += math.log(trigramcount) 
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

      wordScore += trigramScore # + unigramScore + bigramScore

    return characterScore
    return wordScore + characterScore/100

















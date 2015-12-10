import random, string, collections, heapq

# Subsitutes character if mapping exists from current to substitution
# Assumes current and substitution are Capital Strings with no repeating characters
# Case of return character is same as input character
def substitute(character, current, substitution):
    if character.upper() not in current:
        return character
    index_in_substitution = current.find(character.upper())
    if character.isupper():
        return substitution[index_in_substitution]
    return substitution[index_in_substitution].lower()

def getDecryptionKey(encryption_key):
    return "".join([y for (x,y) in sorted(zip(encryption_key, string.ascii_uppercase))])

def encryptCase(text, key):
    textLen = len(text)
    upperText = text.upper()
    chars = list(upperText)
    for i in xrange(textLen): 
        if not chars[i].isalpha(): continue
        chars[i] = key[ord(chars[i]) - 65]
    for i in xrange(textLen):
        if text[i].islower(): chars[i] = chars[i].lower()
    return "".join(chars)

def encrypt(text, key):
    textLen = len(text)
    chars = list(text)
    for i in xrange(textLen): 
        if not chars[i].isalpha(): continue
        chars[i] = key[ord(chars[i]) - 65]
    return "".join(chars)

# Returns random permutation (as a string) of string.ascii_uppercase
def generateKey():
    key = list(string.ascii_uppercase)
    random.shuffle(key)
    return ''.join(key)

# Returnes text with added noise.
# Each alphabet character has noise chance of getting changed to another random alphabet letter of same case
def add_noise(text, noise):
    result = ""
    for letter in text:
        if letter in string.ascii_letters and random.random() < noise:
            random_letter = randomLetter()
            letter = random_letter.upper() if letter.isupper() else random_letter.lower()
        result += letter
    return result

# Returns a random letter. Could be upper or lower case
def randomLetter():
    return random.choice(string.ascii_letters)

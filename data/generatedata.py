import re,  mmap, random, string

NOISE = 0.05 # Probability a letter is changed to any other letter during encryption.

# Add any text sanitation code here so that a text is sanitized before we encrypt it and add noise
# After the first line, text should be a string with no newlines
def sanitize(text):
    text = ' '.join(text.split())

    return text

    ########################################################
    # You probably don't want to edit anything below this. #
    ########################################################

# Uses Regex to pull articles from data
# Returns list of strings
# Each element is the body of a news article
def get_texts(filename):
    texts = []
    with open(filename, 'r+') as f:
        data = mmap.mmap(f.fileno(),0)
        bodyRegex = re.compile("<BODY>([^<]*)</BODY>", re.IGNORECASE)
        matches = bodyRegex.findall(data)
        for match in matches:
            text = "%s" % match
            texts.append(text)
    return texts

# Returns random permutation (as a string) of string.ascii_uppercase
def generateKey():
    key = list(string.ascii_uppercase)
    random.shuffle(key)
    return ''.join(key)

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

# Returns text encrypted using substitution cipher with key as the key
def encrypt(text, key):
    result = ""
    for char in text:
        letter = substitute(char, string.ascii_uppercase, key)
        result += letter
    return result

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

def main():
    keys = open("keys", 'w')
    output = open("substitute", 'w')
    output_noise = open("substitute_noise", 'w')
    original = open("original", "w")

    for i in range(22):
        filename = "reut2-0%02d.sgm" % i 
        texts = get_texts(filename)
        for text in texts:
            text = sanitize(text)
            key = generateKey()
            cipher_text = encrypt(text, key)
            noised = add_noise(cipher_text, NOISE)
            
            keys.write("%s\n" % key)
            output.write("%s\n" % cipher_text)
            output_noise.write("%s\n" % noised)
            original.write("%s\n" % text)


if __name__ == '__main__':
    main()
import re,  mmap, random, string

NOISE = 0.05

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

def encrypt(text, key):
    result = ""
    for char in text:
        letter = substitute(char, string.ascii_uppercase, key)
        result += letter
    return result

def add_noise(text, noise):
    result = ""
    for letter in text:
        if letter in string.ascii_letters and random.random() < noise:
            random_letter = randomLetter()
            letter = random_letter.upper() if letter.isupper() else random_letter.lower()
        result += letter
    return result

def randomLetter():
    return random.choice(string.ascii_letters)

def main():
    output = open("output.csv", 'w')
    output_noise = open("output_noise.csv", 'w')

    for i in range(22):
        filename = "reut2-0%02d.sgm" % i 
        texts = get_texts(filename)
        for text in texts:
            text = ' '.join(text.split())
            key = generateKey()
            cipher_text = encrypt(text, key)
            noised = add_noise(cipher_text, NOISE)
            line =  "%s, %s, %s\n" % (text, key, cipher_text)
            line_noised = "%s, %s, %s\n" % (text, key, noised)
            output.write(line)
            output_noise.write(line_noised)



if __name__ == '__main__':
    main()
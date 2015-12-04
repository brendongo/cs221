import util, string

class Baseline:
    '''
    Baseline generates a key for the cipher_text based on charaacter freuencies.

    It counts the character frequencies of the cipher text and makes a key so that the 
    most common letter in the cipher text maps to the most common letter in english, E, the 
    second most common letter maps to the next most common letter in english, T, etc.

    We got the data for letter frequencies from http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html

    It could have also been done manually on the training data but we would get similar results.
    '''
    
    def __init__(self):
        self.todo = 0
        # From http://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
        self.letters_by_freq = "ETAOINSRHDLUCMFYWGPBVKXQJZ"

    def decrypt(self, text):
        # Count character frequencies of text
        cipher_char_frequency = {}
        for i in string.ascii_uppercase:
            cipher_char_frequency[i] = 0

        for i in text:
            if i in string.ascii_letters:
                cipher_char_frequency[i.upper()] = cipher_char_frequency.get(i.upper()) + 1

        cipher_letters_by_freq = "".join(sorted(cipher_char_frequency, key=cipher_char_frequency.get, reverse=True))
        decryption_key = "".join([y for (x,y) in sorted(zip(self.letters_by_freq, cipher_letters_by_freq))])
        return (util.encrypt(text, decryption_key), decryption_key)
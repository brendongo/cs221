import random, string

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

# Uses substitution cipher to encrypt text
# To encrypt just call encrypt(text, key) where
# key is a permutation of sting.ascii_uppercase
# 
# To decrypt, just call encrypt(text, string.ascii_uppercase, key)
# with the key used to encrypt
def encrypt(text, key, original=string.ascii_uppercase):
    result = ""
    for char in text:
        letter = substitute(char, original, key)
        result += letter
    return result
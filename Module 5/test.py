# 6. Check if string is pangram
def is_pangram(string):
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    if (alphabet.issubset(set(string.lower()))):
        return print('This is Pangram')
    else:
        return print('This is not Pangram')

is_pangram("The quick brown fox jumps over the lazy dog")
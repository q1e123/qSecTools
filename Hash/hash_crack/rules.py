def lowercase(word):
    return word.lower()

def uppercase(word):
    return word.upper()

def reverse(word):
    return word[::-1]

def reflect(word):
    return word+word[::-1]

def duplicate(word):
    return word+word

def en_grammar(word):
    x = [word+'s', word+'ed', word+'ing']
    return [word+'s', word+'ed', word+'ing']

def len_control(word,type,n):
    #less
    if type == 0:
        if len(word)<n:
            return False
        return True
    #greater
    elif type == 1:
        if len(word)<n:
            return False
        return True

def truncate(word,type,n):
    if type == 0:
        return word[:n]
    else:
        return word[n:]

def leet(word):
    leet_dictionary = {
        'a': '4',
        'b': '8',
        'c': '<',
        'd': '|)',
        'e': '3',
        'f': '|=',
        'g': '[',
        'h': '|-|',
        'i': '1',
        'j': '_|',
        'k': '|<',
        'l': '1',
        'm': '^^',
        'n': '|V',
        'o': '0',
        'p': '|o',
        'r': '12',
        's': '5',
        't': '7',
        'u': '|_|',
        'v': '\/',
        'w': '\^/',
        'x': '%',
        'z': '2',
    }
    leet_word = word
    for key, value in leet_dictionary.items():
        leet_word = leet_word.replace(key, value)

    return leet_word

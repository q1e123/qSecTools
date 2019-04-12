import string
import itertools

CHAR_SET = string.printable.replace(string.whitespace,"")

def passwords(length):
    length=int(length)
    possible_passwords = [''.join(i) for i in itertools.product(CHAR_SET, repeat=length)]
    return  possible_passwords
#!/usr/bin/env python3

import sys
from urllib.request import hashlib
import rules
import generators

def get_rule_passwords(word):
    rule_passwords = ["",""]

    rule_func_word_list = [rules.en_grammar]
    rule_func_word_string = [rules.duplicate, rules.lowercase, rules.uppercase, rules.reflect, rules.reverse,rules.leet]

    for f in rule_func_word_list:
        rule_passwords+=f(word)

    for f in rule_func_word_string:
        rule_passwords.append(f(word))

    return rule_passwords

def get_md5(word):
    return hashlib.md5(bytes(word, 'utf-8')).hexdigest()

def get_sha1(word):
    return hashlib.sha1(bytes(word,'utf-8')).hexdigest()

def get_hash(word, crack_type):
    # MD5
    if crack_type == 0:
        return get_md5(word)
    # sha-1
    else:
        return get_sha1(word)

def get_dictionary(crack_type,file_name):
    dictionary = dict()
    passwords = open(file_name, 'r',encoding='latin-1').read().split('\n')
    for password in passwords:
        password_hash = get_hash(password,crack_type)
        dictionary[password_hash] = password
        rule_passwords = get_rule_passwords(password)
        for rule_pass in rule_passwords:
            password_hash = get_hash(rule_pass,crack_type)
            dictionary[password_hash] = rule_pass
    return dictionary

def make_dictionary(hash_type,wordlist):
    dictionary = dict()
    for password in wordlist:
        password_hash = get_hash(password, hash_type)
        dictionary[password_hash] = password
        rule_passwords = get_rule_passwords(password)
        for rule_pass in rule_passwords:
            password_hash = get_hash(rule_pass, hash_type)
            dictionary[password_hash] = rule_pass
    return dictionary

def read_hash_list(hash_file):
    passwords = open(hash_file, 'r').read().split('\n')
    return passwords

def bruteforce(hash_type, length, hash_list, out):
    wordlist = generators.passwords(length)
    dictionary = make_dictionary(hash_type, wordlist)

    cracked_hashes= []
    for hash in hash_list:
        if dictionary.get(hash.lower()):
            print("Hash cracked")
            out.write(hash.lower() + ": ")
            out.write(dictionary[hash.lower()])
            out.write("\n")
            cracked_hashes.append(hash)

    for hash in cracked_hashes:
        hash_list.remove(hash)
    dictionary.clear()

def bruteforce_wrap(hash_type, hash_list, out):
    print("Select mode:")
    print("1. Auto = It will try until the password it's found. WARNING: IT MAY TAKE A HUGE AMMOUNT OF TIME AND A LOT OF MEMORY")
    print("2. Fixed size = It will try all possible passwords of a given length")
    print("3. Maximum length = It will try all possible passwords of length smaller or equals of the given length")
    print("Select mode: ",end='')
    mode = int(input())
    if mode == 1:
        print("Starting Auto mode...")
        current_length = 1
        while len(hash_list)>0:
            print("Current length: ", current_length)
            bruteforce(hash_type,current_length,hash_list,out)
            current_length += 1

    elif mode == 2:
        print("Length = ", end='')
        length = input()
        print("Starting Fixed size length")
        bruteforce(hash_type,length,hash_list,out)

    elif mode == 3:
        print("Maximum length = ", end='')
        max_length = input()
        max_length = int(max_length)
        print("Starting Maximum length mode...")

        for current_length in range(1, max_length+1):
            print("Current length: ", current_length)
            bruteforce(hash_type, current_length, hash_list, out)
            if len(hash_list) == 0:
                break

def crack_hash(hash_list,out,dictionary):
    passwords_not_cracked= []
    passwords_cracked = 0
    print("Starting to crack the hashes")

    hashes = open(hash_list, 'r').read().split('\n')
    for hash in hashes:
        if dictionary.get(hash.lower()):
            print("Hash cracked")
            out.write(hash.lower()+ ": ")
            out.write(dictionary[hash.lower()])
            out.write("\n")
            passwords_cracked+=1
        else:
            print("Couldn't crack the hash")
            passwords_not_cracked.append(hash)

    print(str(passwords_cracked)+ " hashes cracked" )
    print(str(len(passwords_not_cracked))+ " hashes not cracked")

    return passwords_not_cracked

def error_message():
    print("ERROR: You didn't used the script correctly")
    print("Usage: ./hash_crack <hash_type> <input_file> <output_file> [password_list]")
    print("hash_type     = {sha-1,md5}")
    print("input_file    = the file that has the hashes")
    print("output_file   = output file name in witch the cracked hashes will be stored")
    print("password_list = dictionary used to crack the hashes")

def start():
    if len(sys.argv) != 5:
        error_message()
        quit()
    if str(sys.argv[1]) != "sha-1" and str(sys.argv[1]) != "md5":
        error_message()
        quit()

    hash_type  = str(sys.argv[1])
    input_file = str(sys.argv[2])
    output_file= str(sys.argv[3])
    dictionary_file_name = str(sys.argv[4])


    if hash_type == "sha-1":
        hash_type_code = 1
    elif hash_type == "md5":
        hash_type_code = 0

    dictionary = get_dictionary(hash_type_code, dictionary_file_name)
    out = open(output_file, "w+")
    passwords_not_cracked = crack_hash(input_file, out, dictionary)
    dictionary.clear()

    print(passwords_not_cracked)
    if len(passwords_not_cracked) is not 0:
        print("Do you want to brute-force them? WARNING: IT MAY TAKE A LONG TIME (y/n)")
        ans = input()
        if ans.lower() == "y":
            bruteforce_wrap(hash_type_code, passwords_not_cracked, out)

        else:
            print("Exiting...")
            exit()

start()

import json
import random

def rand_key(letter, key_dict):
    return key_dict[letter][random.randint(0, len(key_dict[letter]) - 1)]

def cipher(word, key_dict):
    code = "CIPHER: "
    for c in word:
        code = code + rand_key(c.upper(), key_dict)
    return code

def decipher(code, key_dict):
    srch = ""
    result = ""
    for i in range(len(code)):
        if i % 2 == 0:
            srch = code[i:i+2]
            for value, keys in key_dict.items():
                for item in keys:
                    if item == srch:
                        result = result + value
    return result


with open(".\\dict.json", "r") as f:
    data = json.load(f)
    
    while True:
        print("\nCipher (1) or decipher (2)?\n")
        print("CHOICE: ", end="")
        answer = input()


        print("WORD: ", end="")
        ip = input()
        if answer == "1":
            print(cipher(ip, data) + "\n")
        elif answer == "2":
            val = decipher(ip, data)
            val = val[0] + val[1:].lower()
            print("DECIPHER: " + val + "\n")
    
import sys
import string

#beaufort cipher for chars only
#tbd: encoding non-alpha and numbers

def cipher(text, key):
    result = ""
    key_i = 0
    for i in range(0, len(text)):
        if text[i].isalpha():
            key_element = key[key_i % len(key)]
            mv = ord(key_element) - ord('A')
            current_letter = ord(text[i].upper()) - ord('A')

            if text[i].upper() == text[i]:
                result += chr(ord('A') + (-current_letter + 26 + mv) % 26)
            else:
                result += chr(ord('A') + (-current_letter + 26 + mv) % 26).lower()
            key_i = key_i + 1
        else:
            result += text[i]

    return result

keyword_path = sys.argv[2]

with open(keyword_path, "r") as k:
    keyword = k.read()
    k.close()

textfile_path = sys.argv[1]

with open(textfile_path, "r") as textfile_r:
    text = textfile_r.read()
    new_text = cipher(text, keyword)
    textfile_r.close()

with open(textfile_path, "w") as textfile_w:
    textfile_w.write(new_text)
    print("\n --ORIGINAL TEXT-- \n")
    print(text)
    print("\n --CIPHERED TEXT-- \n")
    print(new_text + "\n")
    textfile_w.close()

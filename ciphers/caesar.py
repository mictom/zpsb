import sys

def transform(letter, shift):
    if letter.upper() == letter:
        l = (ord(letter) - 65 + shift) % 26
        return chr(65 + l)
    else:
        l = (ord(letter) - 97 + shift) % 26
        return chr(97 + l)

if len(sys.argv) < 3:
    print("\nProvide text to cipher in the first argument and number of shifts in the second argument.\n")
    quit()
else:
    try:
        shift = int(sys.argv[1])
        text = sys.argv[2]
    except:
        shift = int(sys.argv[2])
        text = sys.argv[1]

    result = ""
    for i in range(len(text)):
        result = result + transform(text[i], shift)
    print("\nRESULT: " + result + "\n")
import binascii
from colorama import init, Back, Fore
import csv

init()
def text_to_blocks(text, size):
    blocks = []
    while text:
        blocks.append(text[:size])

        text = text[size:]
    return blocks

def get_checksum(text):
    return binascii.crc32(bytes(text, encoding="utf-8")) & 0xffffffff

while True:
    print("__Text to CRC32__\n \
        1: Text to checksum.\n \
        2. CRC validation.\n \
        3. Merge the text back.\n \
        4. Quit.\n \
        Choice: ", end="")
    answer = input()
    if answer not in ("1", "2", "3"):
        print("Choose 1, 2 oe 3 only.")
    elif answer == "1":
        f = open("./textfile.txt", "r")
        content = f.read()

        textblocks = text_to_blocks(content, 50)

        with open("text_to_crc.csv", "w") as csvfile:
            fwriter = csv.writer(csvfile, lineterminator='\n')
            
            fwriter.writerow(["Text", "Checksum", "Checksum validation"])

            for b in textblocks:
                fwriter.writerow([b, str(get_checksum(b))])
        
        csvfile.close()
        f.close()
    
    elif answer == "2":
        with open("text_to_crc.csv", "r") as csvfile:
            freader = csv.reader(csvfile)
            next(freader)

            for row in freader:
                space = 50 - len(row[0])
                if row[1] == str(get_checksum(row[0])):
                    print(row[0] + (space * " ") + " Original: " + row[1] + " Recounted: " + str(get_checksum(row[0])) + " " + Back.GREEN + "CORRECT" + str(space)+ Back.RESET)
                else:
                    print(row[0] + (space * " ") + " Original: " + row[1] + " Recounted: " + str(get_checksum(row[0])) + " " + Back.RED + "WRONG" + Back.RESET)

        csvfile.close()
    elif answer == "3":
        with open("text_to_crc.csv", "r") as csvfile:
            freader = csv.reader(csvfile)
            next(freader)
            for row in freader:
                print(row[0], end="")
            print()
    elif answer == "4":
        quit()

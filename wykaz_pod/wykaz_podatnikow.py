import ijson
import hashlib
import passlib.hash

test_nip = "8393201359"
test_nrb = "84114011530000218221001001"

def generate_hash(value, transformations):
    srch_hash = value
    for _ in range(transformations):
        srch_hash = hashlib.sha512(srch_hash.encode()).hexdigest()
    return srch_hash

def summary(exists, prefix, nip, nrb):
    if exists == True:
        status = "Czynny" if prefix == "skrotyPodatnikowCzynnych.item" else "Zwolniony"
        print("\n \
               Dane podatnika: \n \
               NIP: " + nip + "\n \
               NRB: " + nrb + "\n \
               Status: " + status + "\n"
               )
    else:
        print("\nPodatnik o numerze NIP: " + nip + " i koncie bankowym: " + nrb + " nie istnieje.\n")
    quit()

print("NIP: ", end="")
nip = input() or test_nip
print("Numer konta: ", end="")
nrb = input() or test_nrb

with open("./20200604.json") as f:
    parser = ijson.parse(f)

    date = None
    transformations = None
    for prefix, event, value in parser:
        if prefix == "naglowek.dataGenerowaniaDanych":
            date = value
        elif prefix == "naglowek.liczbaTransformacji":
            transformations = int(value)
        elif date and transformations:
            break

    srch_value = generate_hash(date + nip + nrb, transformations)

    for prefix, event, value in parser:
        if value == srch_value:
            summary(True, prefix, nip, nrb)
            break

    summary(False, None, nip, nrb)
    

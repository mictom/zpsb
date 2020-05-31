import zeep as zp
from colorama import init, Back, Fore
import re
import os
import datetime
import pandas as pd
import xlrd
import xlsxwriter

init()
client = zp.Client(wsdl="https://sprawdz-status-vat.mf.gov.pl/?wsdl")
session_data = pd.DataFrame(columns=["NIP", "Status"])

def generate_report(session):
    writer = pd.ExcelWriter("session_report.xlsx", engine="xlsxwriter")
    session.to_excel(writer, "session_report")

    writer.save()
    print(Back.LIGHTWHITE_EX + Fore.GREEN + "\nSession report has been created successfully.\n")

def print_session(session):
    print("\n" + session.to_markdown() + "\n")

def handle_single_request(nip):
    global session_data
    status = client.service.SprawdzNIP(nip)['Komunikat']

    print(Back.CYAN + nip + ": " + status + "\n")

    #add new line if nip hasn't been logged yet | TBD: add cache
    if session_data["NIP"].any() != nip:
        session_data = session_data.append(pd.DataFrame({"NIP": [nip], "Status":[status]}), ignore_index=True)

def handle_multiple_request(dataframe):
    data = dataframe[dataframe.columns[0]].values.tolist()
    print()
    for i in range(len(data)):
        if validate_nip(str(data[i])) != "":
            print(Back.RED + str(data[i]) + ": Niepoprawny format numeru NIP - linia została pominięta.\n")
            continue
        handle_single_request(str(data[i]))

def validate_nip(nip):
    if len(nip) != 10:
        return (Back.RED + "Numer NIP powinien zawierać 10 cyfr!")
    elif re.match(r'^\d{10}$', nip) == None:
        return (Back.RED + "Podany numer nie powinien zawierać żadnych liter ani znaków specjalnych!")
    else:
        return ""

def usr_get_nip(try_c):
    for i in range(try_c):
        print(Fore.RESET + Back.RESET + "Podaj numer NIP: ", end="")

        nip = input()

        if validate_nip(nip) == "":
            break
        else:
            print(validate_nip(nip))
        if i == 4:
            print("Osiągnieto limit prób. Program się wyłącza.")
            quit()

    return nip

while True:
    print(Fore.RESET + Back.RESET + "Wybierz akcję:\n \
    1: Sprawdź status dla pojedynczego numeru NIP\n \
    2: Sprawdź status dla wielu numerów NIP\n \
    3: Pokaż dane z obecnej sesji\n \
    4: Wygeneruj raport\n \
    5: Wyjdź z programu")
    print("Wybór: ", end="")
    answer = input()
    answers = ("1", "2", "3", "4", "5")

    if answer not in answers:
        print(Back.RED + "Nieprawidłowy wybór. Wybierz akcję poprzez wpisanie cyfry od 1 do 3.")
    elif answer == "1":
        print(Fore.RED + Back.WHITE + "\nPamiętaj, że długość numeru NIP powinna wynosić 10 cyfr i nie powinien zawierać żadnych liter ani znaków specjalnych.")

        nip = usr_get_nip(5)

        print()
        handle_single_request(nip)
        
    elif answer == "2":
        print(Back.RESET + "\nWybierz akcję:\n \
        1: Wypisz numery NIP oddzielając je przecinkami\n \
        2: Wczytaj plik CSV lub XLSX")
        print("Wybór: ", end="")

        answer = input()
        answers = ("1", "2")

        if answer not in answers:
            print(Back.RED + "Nieprawidłowy wybór.")
        elif answer == "1":
            print("Wypisz numery: ", end="")
            items = input().split(",")
            items_cln = [x.strip() for x in items]
            data = pd.DataFrame(items_cln)

        elif answer == "2":
            print(Back.RESET +"\nNumery NIP powinny znajdować się w pierwszej kolumnie. Podaj ścieżkę pliku: ", end="")
            path = input()
            filename, file_ext = os.path.splitext(path)

            if file_ext not in ([".csv", ".xlsx"]):
                print("Niepoprawny typ pliku!")
            elif file_ext == ".csv":
                try:
                    data = pd.read_csv(path)
                except ValueError:
                    print(Back.RED + "Nie ma takiego pliku.")
                    quit()
            elif file_ext == ".xlsx":
                try:
                    data = pd.read_excel(path)
                except ValueError:
                    print(Back.RED + "Nie ma takiego pliku.")
                    quit()
            
        handle_multiple_request(data)

    elif answer == "3":
        print_session(session_data)

    elif answer == "4":
        generate_report(session_data)

    elif answer == "5":
        quit()

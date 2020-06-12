import zeep as zp
import re
import os
import datetime
import pandas as pd
import xlrd
import xlsxwriter
import mysql.connector
import m
from datetime import date
from colorama import init, Back, Fore

#service SprawdzNIPNADzien is not active
#bank acc is not an input to the service
#local db

class Session:
    def __init__(self):
        self.id = id
        self.session_data = pd.DataFrame(columns=["NIP", "Status"])

    def add_to_session(self, NIP):
        if self.session_data["NIP"].any() != NIP.num:
            session_data = session_data.append(pd.DataFrame({"NIP": [NIP.num], "Status":[NIP.status]}), ignore_index=True)

    def generate_report(self):
        writer = pd.ExcelWriter("session_report.xlsx", engine="xlsxwriter") # pylint: disable=abstract-class-instantiated
        session_data.to_excel(writer, "session_report")

        writer.save()
        print(Back.LIGHTWHITE_EX + Fore.GREEN + "\nSession report has been created successfully.\n")
    
    def print_session(self):
        print("\n" + session_data.to_markdown() + "\n")

class NIP:
    def __init__(self, num, bank_acc=None):
        self.num = num
        self.bank_acc = bank_acc
        self.status = ""
        self.status_code = ""

    def save(self):
        print()

    #verify NIP format
    def __validate_nip(self, nip):
        if len(nip) != 10:
            return (Back.RED + "Numer NIP powinien zawierać 10 cyfr!")
        elif re.match(r'^\d{10}$', nip) == None:
            return (Back.RED + "Podany numer nie powinien zawierać żadnych liter ani znaków specjalnych!")
        else:
            return ""

    def get_from_user(self, n_try):
        for i in range(n_try): 
            print(Fore.RESET + Back.RESET + "Podaj numer NIP: ", end="")
            nip = input()
            if __validate_nip(nip) == "":
                print()
                self.num = nip
                break
            else:
                print(__validate_nip(nip))
            if i == 4: 
                #quit the program when too many tries
                print("Osiągnieto limit prób. Program się wyłącza.")
                quit()


    def send_request(self):
        db_msg = db_retrieve_nip(nip, today)
        if db_msg == 0:
            req = client.service.SprawdzNIP(nip)
            status = req['Komunikat']
            db_log_request(nip, today, req['Kod'])
        else:
            status = "juz byl w db"
            print("JUZ Byl w DB") #tutaj odmapowanie
            print(db_msg)

        print(Back.CYAN + nip + ": " + status + "\n")

class Menu:
    def __init__(self):

    def print_main(self):
        while True:
            print(Fore.RESET + Back.RESET + "Wybierz akcję:\n \
            1: Sprawdź status dla pojedynczego numeru NIP\n \
            2: Sprawdź status dla wielu numerów NIP\n \
            3: Pokaż dane z obecnej sesji\n \
            4: Wygeneruj raport\n \
            5: Wyjdź z programu")
            print("Wybór: ", end="")

            choice = input()

            if choice not in ("1", "2", "3", "4", "5"):
                print(Back.RED + "Nieprawidłowy wybór. Wybierz akcję poprzez wpisanie cyfry od 1 do 3.")
            else:
                break
        
        return choice
    
    def print_multicheck_menu():
        print(Back.RESET + "\nWybierz akcję:\n \
        1: Wypisz numery NIP oddzielając je przecinkami\n \
        2: Wczytaj plik CSV lub XLSX")
        print("Wybór: ", end="")
        choice = input()

        if choice not in ("1", "2"):
            print(Back.RED + "Nieprawidłowy wybór.")
            quit()

        return choice


#check if record is in db and return status
def db_retrieve_nip(nip, day, bank_acc=None):
    if bank_acc == None:
        sql = "SELECT status FROM systemy_zintegrowane.status_nip WHERE nip = '%s' AND data = '%s'" % (nip, day)
    else:
        sql = "SELECT status FROM systemy_zintegrowane.status_rachunek_bankowy WHERE nip = '%s' AND data = '%s' AND rachunek_bankowy = '%s'" % (nip, day, bank_acc)
    cursor.execute(sql)
    records = len(cursor.fetchall())
    if records == 0:
        return 0
    else:
        print(data[0][0])
        return records[0][0]

#add a record to db
def db_log_request(nip, day, status, bank_acc=None):
    if bank_acc == None:
        sql = "INSERT INTO systemy_zintegrowane.status_nip (data, nip, status) VALUES ('%s', '%s', '%s');" % (day, nip, status)
    else:
        sql = "INSERT INTO systemy_zintegrowane.status_rachunek_bankowy (data, nip, rachunek_bankowy, status) VALUES ('%s', '%s', '%s', '%s');" % (day, nip, bank_acc, status)
    cursor.execute(sql)
    db.commit()

def handle_multiple_request(dataframe): #dodac ograniczenie 10 zapytan na sekunde
    data = dataframe[dataframe.columns[0]].values.tolist()
    print()
    for i in range(len(data)):
        if validate_nip(str(data[i])) != "":
            print(Back.RED + str(data[i]) + ": Niepoprawny format numeru NIP - linia została pominięta.\n")
            continue
        handle_single_request(str(data[i]))

def load_data_from_file(path):
    _, file_ext = os.path.splitext(path)

    if os.path.isfile(path) == False:
        print(Back.RED + "Należy wskazać plik!")
    elif file_ext not in ([".csv", ".xlsx"]):
        print(Back.RED + "Niepoprawny typ pliku!")
    elif file_ext == ".csv":
        try:
            data = pd.read_csv(path)
            handle_multiple_request(data)
        except ValueError:
            print(Back.RED + "Nie ma takiego pliku.")
            quit()
    elif file_ext == ".xlsx":
        try:
            data = pd.read_excel(path)
            handle_multiple_request(data)
        except ValueError:
            print(Back.RED + "Nie ma takiego pliku.")
            quit()

def main():

    session = Session()
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=m.p
    )
    cursor = db.cursor(buffered=True)

    init() #colorama initation
    client = zp.Client(wsdl="https://sprawdz-status-vat.mf.gov.pl/?wsdl") #soap connection

    today = date.today().strftime("%Y-%m-%d")

    code_mapping = {"N":"Podmiot o podanym identyfikatorze podatkowym NIP nie jest zarejestrowany jako podatnik VAT", 
                    "C":"Podmiot o podanym identyfikatorze podatkowym NIP jest zarejestrowany jako podatnik VAT czynny",
                    "Z":"Podmiot o podanym identyfikatorze podatkowym NIP jest zarejestrowany jako podatnik VAT zwolniony"}

    while True:
        choice = print_menu()

        if choice == "1":
            print(Fore.RED + Back.WHITE + "\nPamiętaj, że długość numeru NIP powinna wynosić 10 cyfr i nie powinien zawierać żadnych liter ani znaków specjalnych.")
            nip = NIP.get_from_user(5)
            handle_single_request(nip)
            
        elif choice == "2":
            choice = print_multicheck_menu

            if choice == "1":
                print("Wypisz numery: ", end="")
                items = input().split(",")
                items_cln = [x.strip() for x in items]
                data = pd.DataFrame(items_cln)

            elif choice == "2":
                print(Back.RESET +"\nNumery NIP powinny znajdować się w pierwszej kolumnie. Podaj ścieżkę pliku: ", end="")
                path = input()
                load_data_from_file(path)

        elif choice == "3":
            session.print_session()

        elif choice == "4":
            session.generate_report()

        elif choice == "5":
            quit()

if __name__ == "__main__":
    main()
import zeep as zp
import re
import os
import datetime
import pandas as pd
import xlrd
import xlsxwriter
import mysql.connector
import string
from datetime import date
from colorama import init, Back, Fore

#service SprawdzNIPNADzien is not active
#bank acc is not an input to the service

class Session:
    def __init__(self):
        self.id = id
        self.session_data = pd.DataFrame(columns=["NIP", "Status", "Konto bankowe"])

    def add_to_session(self, NIP):
        if self.session_data["NIP"].any() != NIP.num:
            self.session_data = self.session_data.append(pd.DataFrame({"NIP": [NIP.num], "Status":[NIP.status], "Konto bankowe":[NIP.bank_acc]}), ignore_index=True)

    def generate_report(self):
        writer = pd.ExcelWriter("session_report.xlsx", engine="xlsxwriter") # pylint: disable=abstract-class-instantiated
        self.session_data.to_excel(writer, "session_report")

        writer.save()
        print(Back.LIGHTWHITE_EX + Fore.GREEN + "\nSession report has been created successfully.\n")
    
    def print_session(self):
        print("\n" + self.session_data.to_markdown() + "\n")

class NIP:
    def __init__(self, num=None):
        self.num = num
        self.bank_acc = None
        self.status = ""
        self.status_code = ""

    def to_text(self):
        if self.bank_acc != None:
            print(Back.CYAN + self.num + " (bank account: " + self.bank_acc + "): " + self.status + "\n")
        else:
            print(Back.CYAN + self.num + ": " + self.status + "\n")

    def validate_iban(self, iban):
        if len(iban) != 26 or iban.isalpha():
            return False
        else:
            return True

    def set_bank_acc(self, new_bank_acc):
        if self.validate_iban(new_bank_acc):
            self.bank_acc = new_bank_acc
        else:
            print(Back.RED + "Podany numer konta bankowego ma zły format!")

    def set_status_code(self, status_code):
        code_mapping = {"N":"Podmiot o podanym identyfikatorze podatkowym NIP nie jest zarejestrowany jako podatnik VAT", 
                        "C":"Podmiot o podanym identyfikatorze podatkowym NIP jest zarejestrowany jako podatnik VAT czynny",
                        "Z":"Podmiot o podanym identyfikatorze podatkowym NIP jest zarejestrowany jako podatnik VAT zwolniony",
                        "I":"Nieprawidłowy Numer Identyfikacji Podatkowej"}
        self.status_code = status_code
        self.status = code_mapping[status_code]

    def validate_nip(self, nip=None):
        if nip == None:
            nip = self.num
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
            if self.validate_nip(nip) == "":
                print()
                self.num = str(nip)
                break
            else:
                print(self.validate_nip(nip))
            if i == 4: 
                #quit the program when too many tries
                print("Osiągnieto limit prób. Program się wyłącza.")
                quit()

    def send_request(self, connection):
        req = connection.service.SprawdzNIP(self.num)
        self.status = req['Komunikat']
        self.status_code = req['Kod']

class App:
    def __init__(self, db, api_connection, session):
        self.db = db
        self.choice = ""
        self.imported_file_path = ""
        self.cursor = db.cursor(buffered=True)
        self.client = api_connection
        self.session = session

    def save_to_db(self, NIP):
        if NIP.bank_acc == None:
            sql = "INSERT INTO systemy_zintegrowane.status_nip (data, nip, status) VALUES (%s, %s, %s);"
            values = (date.today().strftime("%Y-%m-%d"), NIP.num, NIP.status_code)
        else:
            sql = "INSERT INTO systemy_zintegrowane.status_rachunek_bankowy (data, nip, status, rachunek_bankowy) VALUES (%s, %s, %s, %s);"
            values = (date.today().strftime("%Y-%m-%d"), NIP.num, NIP.status_code, NIP.bank_acc)

        self.cursor.execute(sql, values)
        self.db.commit()

    def set_choice(self, c):
        self.choice = c

    def print_main_menu(self):
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
                self.set_choice(choice)
                return
    
    def print_multicheck_menu(self):
        print(Back.RESET + "\nWybierz akcję:\n \
        1: Wypisz numery NIP oddzielając je przecinkami\n \
        2: Wczytaj plik CSV lub XLSX")
        print("Wybór: ", end="")
        choice = input()

        if choice not in ("1", "2"):
            print(Back.RED + "Nieprawidłowy wybór.")
            quit()
        else:
            self.set_choice(choice)
            return

    def nip_instr(self):
        print(Fore.RED + Back.WHITE + "\nPamiętaj, że długość numeru NIP powinna wynosić 10 cyfr i nie powinien zawierać żadnych liter ani znaków specjalnych.")
        print(Fore.RESET + Back.RESET + "\nCzy chcesz sprawdzić NIP wraz z kontem bankowym? \n \
            1: Tak\n \
            2: Nie")
        print("Wybór: ", end="")
        choice = input()

        if choice not in ("1", "2"):
            print(Back.RED + "Nieprawidłowy wybór.")
            quit()
        else:
            self.set_choice(choice)
            return

    def path_instr(self):
        print(Back.RESET +"\nNumery NIP powinny znajdować się w pierwszej kolumnie. Podaj ścieżkę pliku: ", end="")
        self.imported_file_path = input()

    def load_data_from_file(self):
        _, file_ext = os.path.splitext(self.imported_file_path)

        if os.path.isfile(self.imported_file_path) == False:
            print(Back.RED + "Należy wskazać plik!")
        elif file_ext not in ([".csv", ".xlsx"]):
            print(Back.RED + "Niepoprawny typ pliku!")
        elif file_ext == ".csv":
            try:
                data = pd.read_csv(self.imported_file_path)
                self.handle_multiple_request(data)
            except ValueError:
                print(Back.RED + "Nie ma takiego pliku.")
                quit()
        elif file_ext == ".xlsx":
            try:
                data = pd.read_excel(self.imported_file_path)
                self.handle_multiple_request(data)
            except ValueError:
                print(Back.RED + "Nie ma takiego pliku.")
                quit()
    
    def load_from_user_list(self):
        print("Wypisz numery: ", end="")
        items = input().split(",")
        items_cln = [x.strip() for x in items]
        data = pd.DataFrame(items_cln)
        self.handle_multiple_request(data)

    def db_retrieve_nip(self, nip, day, bank_acc=None):
        if bank_acc == None:
            sql = "SELECT status FROM systemy_zintegrowane.status_nip WHERE nip = %s AND data = %s"
            values = (nip.num, day)
        else:
            sql = "SELECT status FROM systemy_zintegrowane.status_rachunek_bankowy WHERE nip = %s AND data = %s AND rachunek_bankowy = %s"
            values = (nip.num, day, nip.bank_acc)
        self.cursor.execute(sql, values)
        records = self.cursor.fetchall()
        if len(records) == 0:
            return 0
        else:
            return records[0][0]

    def handle_multiple_request(self, dataframe): #dodac ograniczenie 10 zapytan na sekunde
        
        print("Czy sprawdzić również konta bankowe? Y/N")
        kb = input()

        data = dataframe[dataframe.columns[0]].values.tolist()
        bank_data = dataframe[dataframe.columns[1]].values.tolist()
        print()

        for i in range(len(data)):
            nip = NIP(num=str(data[i]))
    
            if nip.validate_nip() != "":
                print(Back.RED + nip.num + ": Niepoprawny format numeru NIP - linia została pominięta.\n")
                continue
            
            if str(bank_data[i]) != "nan":
                print(bank_data[i])
                nip.set_bank_acc(str(bank_data[i]))
                qry_result = self.db_retrieve_nip(nip, date.today().strftime("%Y-%m-%d"), nip.bank_acc)
            else:
                qry_result = self.db_retrieve_nip(nip, date.today().strftime("%Y-%m-%d"))

            if qry_result != 0:
                nip.set_status_code(qry_result)
                nip.to_text()
                self.session.add_to_session(nip)
                continue

            nip.send_request(self.client)
            self.session.add_to_session(nip)
            self.save_to_db(nip)
            
            nip.to_text()

def main():

    session = Session()

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password= "eloelo123",
        auth_plugin='mysql_native_password'
    )

    client = zp.Client(wsdl="https://sprawdz-status-vat.mf.gov.pl/?wsdl") #soap connection

    app = App(db, client, session)

    init() #colorama initation

    while True:
        app.print_main_menu()

        if app.choice == "1":

            app.nip_instr()
            if app.choice == "1":
                nip = NIP()
                print("Podaj konto bankowe: ", end="")
                bank_acc = input()
                if nip.set_bank_acc(bank_acc) == False:
                    continue
                nip.get_from_user(n_try=5)
                qry_result = app.db_retrieve_nip(nip, date.today().strftime("%Y-%m-%d"), bank_acc)
            elif app.choice == "2":
                nip = NIP()
                nip.get_from_user(n_try=5)
                qry_result = app.db_retrieve_nip(nip, date.today().strftime("%Y-%m-%d"))
                
            if qry_result == 0:
                nip.send_request(client)
                app.save_to_db(nip)
                nip.to_text()
                session.add_to_session(nip)
            else:
                nip.set_status_code(qry_result)
                nip.to_text()
            
        elif app.choice == "2":
            app.print_multicheck_menu()

            if app.choice == "1":
                app.load_from_user_list()

            elif app.choice == "2":
                app.path_instr()
                app.load_data_from_file()

        elif app.choice == "3":
            session.print_session()

        elif app.choice == "4":
            session.generate_report()

        elif app.choice == "5":
            quit()

if __name__ == "__main__":
    main()
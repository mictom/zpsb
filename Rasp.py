import gspread
import pandas as pd
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk

#konfiguracja api
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('.//cre.json', scope) #credentials

client = gspread.authorize(creds) #autoryzacja

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qS-xrQJD6oIl8bouIoBJciYx-mGd-cgOeIfKg2b3S44/edit#gid=0")
ws = sheet.get_worksheet(0)

#konfiguracja tkinter
root = tk.Tk()	#stworzenie obiektu biblioteki tkinter
root.title("Zadania")

canvas = tk.Canvas(root, borderwidth=0, background="#ffffff") #stworzenie obiektu canvas
sb = tk.Scrollbar(root, orient='vertical', command=canvas.yview, jump=1) #stworzenie suwaka

root.attributes("-fullscreen", True) #ustawienie pełnego ekranu
root.configure(background='white') #ustaw białego tła aplikacji
root.bind("<Escape>", quit)	#wyjście z aplikacji przy użyciu klawisza Escape
x = root.winfo_screenwidth() / 2 #środek szerokości ekranu
y = root.winfo_screenheight() / 2 #środek wysokości ekranu
root.geometry("+%d+%d" % (x, y)) #geomteria ekranu mająca początek na jego środku

today = datetime.date.today().strftime("%d.%m.%Y")

#zapisanie zmian w Google Sheets i usuniecie przycisku
def complete_task(button):
    row_to_update = ws.find(button["text"], in_column=2).row
    ws.update_cell(row_to_update, 3, "YES")
    button.destroy()

#dobranie zadań i rysowanie przycisków
def log_taks():
    btn_count = 1
    drawn_btns = [] 
    recs = ws.get_all_records() #pobierz wszystkie zadania
    for r in recs:
        if r["DAY"] == today and r["COMPLETED"] == "" and drawn_btns.count(r["TASK"]) == 0 and r["TASK"] != "": #wyfiltruj tylko zadania na dzisiaj, które nie zostały ukończone
            btn = tk.Button(text=r["TASK"], bg='white', border=0.5, relief = "flat") #tworznie przycisku
            canvas.create_window(0, btn_count * 30, anchor='nw', window=btn, height=30, width=canvas.winfo_width()) #umieszczenie przycisku w obiekcie canvas
            btn.config(command=lambda b=btn: complete_task(b)) #dodanie funkcji callback do przycisku
            btn_count = btn_count + 1
            drawn_btns.append(r["TASK"])

#rysowanie nowego obiketu canvas
def redraw_canvas():
    canvas.config(yscrollcommand=sb.set, scrollregion=canvas.bbox('all'))
    canvas.pack(fill='both', expand=True, side='left')
    sb.pack(fill='y', side='right')

#pętla odświeżająca dane co 5 sekund
def refresh_app():
    canvas.delete("all")
    log_taks()
    redraw_canvas()
    root.after(5000, refresh_app)

refresh_app()
tk.mainloop()

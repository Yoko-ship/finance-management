import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import time

connection = sqlite3.connect("finance.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS finance(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  Initial INTEGER,
                  ProductName TEXT,
                  ProductPrice INTEGER,
                  Overall INTEGER,
                  DATA INTEGER
    )
""")

now = datetime.now()
formatted_data = now.strftime("%y.%m.%d %H:%M")

productPricing = None
productNaming = None
Initial = None
selected_tab = None

def load_all_informations(listbox):
    cursor.execute("SELECT * FROM finance")
    all_informations = cursor.fetchall()
    listbox.delete(0, tk.END)

    for row in all_informations:
        row_text = f"ID: {row[0]} || Сумма: {row[1]} || Товар: {row[2]} || Цена: {row[3]} || Итого: {row[4]} || Дата: {row[5]}"
        listbox.insert(tk.END, row_text)

def on_tab_selected(event):
    global selected_tab
    selected_tab = event.widget.tab(event.widget.index("current"))["text"]

def confirm():
    global productNaming, productPricing, Initial
    try:
        Initial = int(entryInitial.get())
        productPricing = int(entryProductPrice.get())
        productNaming = entryProductName.get()
    except ValueError:
        error_label.config(text="Пожалуйста, введите все данные.")
        return
    
    root.withdraw()
    if selected_tab == "Расходы":
        cursor.execute("SELECT Overall, Initial FROM finance")
        overallPrice = cursor.fetchall()

        if overallPrice:
            last_entry = overallPrice[-1]
            currentPrice = int(last_entry[0])
            initialAmount = int(last_entry[1])
            overall = currentPrice - productPricing
            cursor.execute("INSERT INTO finance (Initial, ProductName, ProductPrice, Overall, DATA) VALUES(?,?,?,?,?)",
                           (initialAmount, productNaming, productPricing, overall, formatted_data))
        else:
            overall = Initial - productPricing
            cursor.execute("INSERT INTO finance (Initial, ProductName, ProductPrice, Overall, DATA) VALUES(?,?,?,?,?)",
                           (Initial, productNaming, productPricing, overall, formatted_data))

    connection.commit()
    entryInitial.delete(0, tk.END)
    entryProductName.delete(0, tk.END)
    entryProductPrice.delete(0, tk.END)
    time.sleep(2)  
    root.deiconify()  

def incomeAdd():
    global userIncome
    try:
        userIncome = int(income_add_entry.get())
    except ValueError:
        error_income.config(text="Пожалуйста, введите данные.")
        return

    root.withdraw()
    if selected_tab == "Доходы":
        cursor.execute("SELECT Initial, id, ProductPrice, Overall FROM finance")
        allInformations = cursor.fetchall()
        if allInformations:
            lastEntry = allInformations[-1]
            currentAmount = lastEntry[0]
            current_id = lastEntry[1]
            price_product = lastEntry[2]
            overall_price = lastEntry[3]

            initialNumber = userIncome + currentAmount
            overall_price = initialNumber - price_product 
            cursor.execute("UPDATE finance SET Initial = ?, Overall = ?, DATA =? WHERE id =?", (initialNumber, overall_price, formatted_data, current_id))

    connection.commit()
    income_add_entry.delete(0, tk.END)
    time.sleep(2)
    root.deiconify()  

root = tk.Tk()
root.title("Finance-app")
root.geometry("400x400")
root.configure(bg="#f0f0f0")


style = ttk.Style()
style.configure("TNotebook", background="#e0e0e0")
style.configure("TNotebook.Tab", background="#ddd", padding=(10, 5))
style.map("TNotebook.Tab", background=[("selected", "#ccc")])


notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)


expense_label = ttk.Frame(notebook)
notebook.add(expense_label, text="Расходы")

labelInitial = tk.Label(expense_label, text="Изначальная сумма", bg="#f0f0f0")
labelInitial.pack(pady=5)
entryInitial = tk.Entry(expense_label)
entryInitial.pack(pady=5)

labelProductName = tk.Label(expense_label, text="Названия товара", bg="#f0f0f0")
labelProductName.pack(pady=5)
entryProductName = tk.Entry(expense_label)
entryProductName.pack(pady=5)

labelProductPrice = tk.Label(expense_label, text="Цена товара", bg="#f0f0f0")
labelProductPrice.pack(pady=5)
entryProductPrice = tk.Entry(expense_label)
entryProductPrice.pack(pady=5)

error_label = tk.Label(expense_label, text="", fg="red", bg="#f0f0f0")
error_label.pack()

button = tk.Button(expense_label, text="Подтвердить", command=confirm, bg="#4CAF50", fg="white", activebackground="#45A049")
button.pack(pady=10)

expenses_listBox = tk.Listbox(expense_label, width=100, height=10)
expenses_listBox.pack(fill="both", expand=True, pady=5)

load_button = tk.Button(expense_label, text="Загрузить данные", command=lambda: load_all_informations(expenses_listBox), bg="#2196F3", fg="white", activebackground="#1976D2")
load_button.pack(pady=5)

load_all_informations(expenses_listBox)

#  Доходы
income_label = ttk.Frame(notebook)
notebook.add(income_label, text="Доходы")

income_add = tk.Label(income_label, text="Доход:", bg="#f0f0f0")
income_add.pack(pady=5)
income_add_entry = tk.Entry(income_label)
income_add_entry.pack(pady=5)

error_income = tk.Label(income_label, text="", fg="red", bg="#f0f0f0")
error_income.pack()

income_button = tk.Button(income_label, text="Подтвердить", command=incomeAdd, bg="#4CAF50", fg="white", activebackground="#45A049")
income_button.pack(pady=10)

income_listBox = tk.Listbox(income_label)
income_listBox.pack(fill="both", expand=True, pady=5)

load_button_income = tk.Button(income_label, text="Загрузить данные", command=lambda: load_all_informations(income_listBox), bg="#2196F3", fg="white", activebackground="#1976D2")
load_button_income.pack(pady=5)

load_all_informations(income_listBox)

notebook.bind("<<NotebookTabChanged>>", on_tab_selected)

root.mainloop()

connection.commit()
connection.close()

import tkinter as tk
from tkinter import ttk
import requests
import json
#Библеотека

url = 'https://www.cbr-xml-daily.ru/daily_json.js'

window = tk.Tk()
window.title("Currency Converter")
window.geometry("400x300")


label_result = tk.Label(text="", bg="#f0f0f0")
label_result.pack(pady=5)

tk.Label(text="Из", bg="#f0f0f0").pack(pady=5)


currencies  = ["AED","CNY","USD","EUR","INR","KZT","CAD","RUB"]

first_choice = ttk.Combobox(values=currencies)
first_choice.pack(pady=5)

tk.Label(text="В", bg="#f0f0f0").pack(pady=5)

second_choice = ttk.Combobox(values=currencies)
second_choice.pack(pady=5)

quantity_entry = tk.Entry(width=10)
quantity_entry.pack(pady=5)

response = requests.get(url)
list_currency = response.json()

list_currency["Valute"]["RUB"] = {"Value": 1, "Nominal": 1}

def calculate():
   try:
      if float(quantity_entry.get())>0:
            if response.status_code == 200:
               first_value = list_currency["Valute"][first_choice.get()]["Value"]/list_currency["Valute"][first_choice.get()]["Nominal"]
               second_value = list_currency["Valute"][second_choice.get()]["Value"]/list_currency["Valute"][second_choice.get()]["Nominal"]
               answer = float(quantity_entry.get())*first_value/second_value
               label_result.config(text=str(round(answer,2)))
         
               with open("history.json", "r", encoding="utf-8") as file:
                  try:
                     history_data = json.load(file)
                  except:
                     history_data = []
         
               history_data.append({
                  "from": first_choice.get(),
                  "to": second_choice.get(),
                  "amount": float(quantity_entry.get()),
                  "result": round(answer,2)
               })

               with open("history.json", "w", encoding="utf-8") as f:
                  json.dump(history_data, f, ensure_ascii=False, indent=4)
            else:
               print(f'Ошибка: {response.status_code}')
      else:
         print("Введите положительное число")
         label_result.config(text="Введите положительное число")
   except KeyError:
      print("Ошибка: валюты нет в списке")
      label_result.config(text="Ошибка: валюты нет в списке")
   except ValueError:
      print("Введите целое положительное число")
      label_result.config(text="Введите целое положительное число")
   except TypeError:
      print("Введите целое положительное число")
      label_result.config(text="Введите целое положительное число")
tk.Button(text="Конвертировать", command=calculate, bg="#4CAF50", fg="white").pack(pady=20)

window.mainloop()

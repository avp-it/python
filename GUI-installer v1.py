# GUI программа для установки сертов и САС
# import pyautogui
# import pygetwindow as gw
# import ctypes
# import keyboard
# import pyperclip #позволяет копировать в буфер
# import psutil #позволяет закрывать процесс
# import shutil
# import os.path
# import pathlib
# from time import sleep
import os
import subprocess  #позволяет вызывать bat файлы
import tkinter as tk
from tkinter import *
from tkinter import ttk, Canvas, Frame, BOTH
# from tkinter import messagebox as mb
# from tkinter.scrolledtext import ScrolledText
from export_vipnet import *
from reg_csp import *
from Copy_cont import *
from copy_cont2 import *

# Блок настройки параметров окна
root = Tk()  # окно
root.title("Установка компонентов")  # титул окна
root.geometry("600x360")  # размер окна
root.resizable(False, True)  # изменяемый размер окна по ширине и высоте
root.geometry(f"+{(root.winfo_screenwidth() - 500) // 2}+{(root.winfo_screenheight() - 500) // 2}")
# appdir = pathlib.Path(__file__).parent.resolve()
# root.iconbitmap(os.path.join(appdir,'icon.ico'))
# root.iconbitmap("C:/vampire.ico")
# root.eval('tk::PlaceWindow . center')
# root.attributes("-alpha", 0.8) # прозрачность окна в процентах
# root.configure(bg='#B6E2E5') # цвет фона окна


def func():
    actions = [(reg_CSP.get(), csp_registration),
               (instal_cert_and_crl.get(), lambda: subprocess.call(r"\10.77.60.13InstalPlaksinAVBatinstallinstall_cer.bat")),
               (copy_cont.get(), copy_contANDcerts_first),
               (copy_cont2.get(), copy_contANDcerts_second),
               (copy_DEconfig.get(), lambda: subprocess.call(r"\10.77.60.13InstalPlaksinAVBatinstallcopy_DEconfig.bat")),
               (start_DE.get(), lambda: os.startfile(r"C:ProgramDataCrypto+DECrypto+DE.exe")),
               (export_vipnet.get(), export)]

    for condition, action in actions:
        if condition:
            action()


ttk.Style().configure(".",
                      font="helvetica 13",
                      foreground="#000000",
                      padding=8)  #background="#B6E2E5")
position = {"padx": 5, "pady": 2, "anchor": NW}

# Функция для создания Checkbutton
def create_checkbutton(text, variable):
    checkbox = ttk.Checkbutton(text=text, variable=variable)
    checkbox.pack(**position)
    return checkbox

def create_button(text, command, padx=5, pady=5):
    button = ttk.Button(root, text=text, command=command)
    button.pack(**position)
    return button

# Создание переменных
reg_CSP = IntVar()
instal_cert_and_crl = IntVar()
copy_cont = IntVar()
copy_cont2 = IntVar()

# Создание Checkbuttons
create_checkbutton("Зарегистрировать ViPNet CSP", reg_CSP)
create_checkbutton("Установить корневые сертификаты и списки отзыва", instal_cert_and_crl)
create_checkbutton("Установить ключ и сертификат пользователя (Переустановка)", copy_cont)
create_checkbutton("Установить ключ и сертификат пользователя (Первичная установка или плановая смена)", copy_cont2)
create_button("Выполнить отмеченное", func, padx=5, pady=5)
create_button("Выход", root.destroy, padx=5, pady=5)

root.mainloop()

# reg_CSP = IntVar()
# checkbtn = ttk.Checkbutton(text="Зарегистрировать ViPNet CSP", variable=reg_CSP).pack(**position)

# instal_cert_and_crl = IntVar()
# checkbtn = ttk.Checkbutton(text="Установить корневые сертификаты и списки отзыва", variable=instal_cert_and_crl).pack(**position)

# copy_cont = IntVar()
# checkbtn = ttk.Checkbutton(text="Установить ключ и сертификат пользователя\n(Переустановка)",
#     variable=copy_cont).pack(**position)

# copy_cont2 = IntVar()
# checkbtn = ttk.Checkbutton(text="Установить ключ и сертификат пользователя\n(Первичная установка или плановая смена)",
#     variable=copy_cont2).pack(**position)

# # copy_PLANsettings = IntVar()
# # checkbtn = ttk.Checkbutton(text="Добавить задачу обновления Crypto+DE в планировщик", variable=copy_PLANsettings).pack(**position)

# copy_DEconfig = IntVar()
# checkbtn = ttk.Checkbutton(text="Применить настройки Crypto+DE", variable=copy_DEconfig).pack(**position)

# start_DE = IntVar()
# checkbtn = ttk.Checkbutton(text="Запустить Crypto+DE", variable=start_DE).pack(padx=15, pady=2, anchor=NW)

# export_vipnet = IntVar()
# checkbtn = ttk.Checkbutton(text="Экспортировать настройки и ключи ViPNet на сервер", variable=export_vipnet).pack(padx=5, pady=20, anchor=NW)

# btn1 = ttk.Button(text="Выполнить отмеченное", command=func).pack(**position)

# btn2 = ttk.Button(root, text="Выход", command=root.destroy).pack(**position)

# st = ScrolledText(root, width=50,  height=10)
# st.pack(fill=BOTH, side=LEFT, expand=True)



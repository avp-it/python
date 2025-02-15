"""Скрипт для автоматического обновления сертфиката пользователя из каталога на сервере. Добавлен перезапуск DE и установка корневиков"""
import os
import sys
import shutil
import psutil
from os import startfile
from datetime import datetime
from time import sleep
import tkinter as tk
from tkinter import messagebox
# from inst_wmail_cert import choose_cert
from copy_de_settings import get_file_version, copy_config

def show_message(message):
    """Отображает сообщение во всплывающем окне."""
    root.lift()
    root.attributes('-topmost', True)
    messagebox.showinfo("Сообщение", message)
    root.destroy()

def clear_directory(directory):
    """Удаляет все файлы в указанной директории."""
    if os.path.exists(directory):
        for f in os.listdir(directory):
            os.remove(os.path.join(directory, f))

def copy_certificates(src, dest):
    """Копирует сертификаты из src в dest."""
    for f in os.listdir(src):
        shutil.copy2(os.path.join(src, f), dest)

def log_report(user_folders, status):
    """Записывает отчет."""
    current_time = datetime.now().strftime('%d.%m.%Y %H:%M')
    with open('//10.77.60.13/Share/Plaksin/Reports/install_new_certs.txt', 'a') as file:
        for user_folder in user_folders:
            username = os.path.basename(user_folder).split('.')[0]
            file.write(f"{username} {current_time} {status}\n")

def start_cde():
    """Запускает C+DE"""
    de_path = r"C:\ProgramData\Crypto+DE"
    if os.path.isdir(de_path):
        os.startfile(os.path.join(de_path, "Crypto+DE.exe"))
    else:
        # log_report(user_folders, login, ">> Crypto+DE не установлен")
        sys.exit()


def install():
    """Основной модуль."""

    login = os.getlogin()
    homepath = os.getenv('USERPROFILE')
    contacts_path = os.path.normpath(os.path.join(homepath, 'contacts'))

    user_folders = [folder for folder in os.listdir(contacts_path) if folder != 'desktop.ini']
    username_folder = os.path.basename(user_folders[0]).split('.')[0]
    # username_folder = [os.path.splitext(file)[0] for file in os.listdir(os.path.join(homepath, 'contacts')) if file != 'desktop.ini'][0]


    src_dir = os.path.join('//10.77.60.20/Users', username_folder, 'User_path', login)
    src_dir_my = os.path.join(src_dir, 'My')
    src_dir_cont = os.path.join(src_dir, 'AppData/Local/InfoTeCS/Containers')

    dest_dir_my = os.path.join(homepath, 'AppData/Roaming/Microsoft/SystemCertificates/My')
    dest_dir_cont = os.path.join(homepath, 'AppData/Local/Infotecs/Containers')

    # Проверка доступа к каталогу
    if not os.access(src_dir, os.R_OK):
        # input("Ключи не найдены или к удаленному каталогу с ключами нет доступа\n\nНажмите 'Enter' для выхода")
        messagebox.showinfo("Сообщение", "Ключи не найдены или к удаленному каталогу с ключами нет доступа")
        log_report(user_folders, ">> ключ не установлен")
        return

    # Закрытие УЭПШа, если открыт
    for process in psutil.process_iter():
        if process.name() == 'Crypto+DE.exe':
            process.terminate()

    # Копирование конфига DE
    file_path = r"C:/ProgramData/Crypto+DE/Crypto+DE.exe"
    version = get_file_version(file_path)
    copy_config(version)

    # Очистка каталогов старых сертификатов и ключей
    clear_directory(os.path.join(dest_dir_my, 'Certificates'))
    clear_directory(os.path.join(dest_dir_my, 'Keys'))
    if os.path.exists(dest_dir_cont):
        shutil.rmtree(dest_dir_cont)

    # Установка нового ключа и сертификата
    copy_certificates(os.path.join(src_dir_my, 'Certificates'), os.path.join(dest_dir_my, 'Certificates'))

    keys_src = os.path.join(src_dir_my, 'Keys')
    keys_dest = os.path.join(dest_dir_my, 'Keys')

    if not os.path.exists(keys_dest):
        shutil.copytree(keys_src, keys_dest)
    else:
        copy_certificates(keys_src, keys_dest)

    shutil.copytree(src_dir_cont, dest_dir_cont)

    # print(f"Сертификат пользователя {username_folder} установлен")
    # input(f"Сертификат пользователя '{username_folder}' обновлен\n\nНажмите 'Enter' для выхода")

    root = tk.Tk()
    root.withdraw()  # Скрываем главное окно
    messagebox.showinfo("Сообщение", "Новый сертификат установлен")

    log_report(user_folders, ">> ключ установлен")

    start_cde()

    # sleep(120)

    # choose_cert()
if __name__ == "__main__":
    install()

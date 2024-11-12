"""Установка CDE с выбором версии"""
import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def choose_version():
    root = tk.Tk()
    root.withdraw()  # Скрываем главное окно

    # Всплывающее окно с выбором
    choice = messagebox.askyesnocancel("Выбор версии", "Да - установить версию 5.0.1 (Основная)\nНет - установить версию 4.4.3 (для ЕЦП)\nОтмена - выход без установки")

    return choice

def main():
    # Получаем путь к директории, в которой находится EXE
    dir_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Указываем имена установочных файлов
    installer_name_v5 = "CryptoPlusDESetup.5.0.1.exe"
    installer_name_v4 = "CryptoPlusDESetup.4.4.3.exe"

    choice = choose_version()

    if choice is None:  # Отмена
        return
    elif choice:  # Да, v5
        installer_name = installer_name_v5
    else:  # Нет, v4
        installer_name = installer_name_v4

    # Указываем полный путь к установочному файлу
    installer_file = os.path.join(dir_path, "installers", installer_name)

    # Проверяем наличие файла
    if os.path.exists(installer_file):
        print(f"Производится установка CDE версии {installer_name}. ")
        subprocess.run([installer_file, '/S', '-installmode=pfr'], check=True)

        input("Установка завершена. Нажмите Enter.")
    else:
        input('Установочный файл не найден.')

if __name__ == "__main__":
    main()



"""Получение версии программы CDE и копирование настроек"""
import pefile
import shutil
import os
import sys

def get_file_version(file_path):
    try:
        pe = pefile.PE(file_path)
        vs_fixed_file_info = pe.VS_FIXEDFILEINFO[0]
        file_version = (
            (vs_fixed_file_info.FileVersionMS >> 16),
            (vs_fixed_file_info.FileVersionMS & 0xFFFF),
            (vs_fixed_file_info.FileVersionLS >> 16),
            (vs_fixed_file_info.FileVersionLS & 0xFFFF),
        )
        return ".".join(map(str, file_version))
    except Exception as e:
        print(f"Ошибка при получении версии: {e}")
    return None

def copy_config(version):
    # Получаем путь к каталогу, в котором находится исполняемый файл
    dir_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Указываем конфигурационные пути относительно каталога с exe
    config_paths = {
        "4.4.3.0": os.path.join(dir_path, "installers/ConfigTechnoserv"),
        "5.0.1.0": os.path.join(dir_path, "installers/ConfigPFR_5.0.1.0"),
    }

    if version in config_paths:
        destination = os.path.join(os.path.expanduser("~"), "AppData", "Local")
        shutil.copytree(config_paths[version], destination, dirs_exist_ok=True)
        print(f"Скопирована конфигурация для версии {version}")
    else:
        print("Версия не распознана или отсутствует.")

file_path = r"C:/ProgramData/Crypto+DE/Crypto+DE.exe"
version = get_file_version(file_path)
copy_config(version)





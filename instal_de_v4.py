"""Установка CDE с выбором версии и копированием настроек"""
import os
import sys
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox
from time import sleep
import pefile

"""Создание окна с вопросом о выборе версии"""
def choose_version():
    root = tk.Tk()
    root.withdraw()  # Скрываем главное окно

    # Всплывающее окно с выбором
    choice = messagebox.askyesnocancel(
        "Выбор версии",
        "Да - установить версию 5.0.1 (Основная)\nНет - установить версию 4.4.3 (для ЕЦП)\nОтмена - выход без установки",
    )
    root.destroy()  # Завершаем работу Tkinter
    return choice

"""Получение версии установленной программы"""
def get_file_version(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден.")
            return None
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

"""Копирование конфига в зависимости от версии программы"""
def copy_config(version):
    file_path = r"C:/ProgramData/Crypto+DE/Crypto+DE.exe"
    version = get_file_version(file_path)

    # Получаем путь к каталогу, в котором находится исполняемый файл
    dir_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    config_paths = {
        "4.4.3.0": os.path.join(dir_path, "sources/CryptoPlusDESetup.4.4.3_config"),
        "5.0.1.0": os.path.join(dir_path, "sources/CryptoPlusDESetup.5.0.1_config"),
    }

    if version in config_paths:
        destination = os.path.join(os.path.expanduser("~"), "AppData", "Local")
        shutil.copytree(config_paths[version], destination, dirs_exist_ok=True)
        sleep(1)
        print(f"> Скопирована конфигурация для версии {version}")
    else:
        print("> Версия не распознана или отсутствует.")

"""Основной цикл: Установка программы и копирование конфига"""
def install_de():
    dir_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    installer_name_v5 = "CryptoPlusDESetup.5.0.1.exe"
    installer_name_v4 = "CryptoPlusDESetup.4.4.3.exe"

    choice = choose_version()

    if choice is None:  # Отмена
        return
    elif choice:  # Да, v5
        installer_name = installer_name_v5
    else:  # Нет, v4
        installer_name = installer_name_v4

    installer_file = os.path.join(dir_path, "sources", installer_name)

    if os.path.exists(installer_file):
        print(f"> Будет выполнена установка C+DE версии {installer_name}. ")
        sleep(1)
        try:
            subprocess.run([installer_file, '/S', '-installmode=pfr'], check=True)
            sleep(1)
            print("> Установка завершена.")
        except subprocess.CalledProcessError as e:
            print(f"> Ошибка при установке: {e}")
    else:
        print("> Установочный файл не найден.")

    # Получение версии и копирование конфигурации
    file_path = r"C:/ProgramData/Crypto+DE/Crypto+DE.exe"
    version = get_file_version(file_path)
    if version:
        copy_config(version)


if __name__ == "__main__":
    install_de()







# """Получение версии программы CDE и копирование настроек"""
# import pefile
# import shutil
# import os
# import sys

# def get_file_version(file_path):
#     try:
#         pe = pefile.PE(file_path)
#         vs_fixed_file_info = pe.VS_FIXEDFILEINFO[0]
#         file_version = (
#             (vs_fixed_file_info.FileVersionMS >> 16),
#             (vs_fixed_file_info.FileVersionMS & 0xFFFF),
#             (vs_fixed_file_info.FileVersionLS >> 16),
#             (vs_fixed_file_info.FileVersionLS & 0xFFFF),
#         )
#         return ".".join(map(str, file_version))
#     except Exception as e:
#         print(f"Ошибка при получении версии: {e}")
#     return None

# def copy_config(version):
#     # Получаем путь к каталогу, в котором находится исполняемый файл
#     dir_path = os.path.dirname(os.path.abspath(sys.argv[0]))

#     # Указываем конфигурационные пути относительно каталога с exe
#     config_paths = {
#         "4.4.3.0": os.path.join(dir_path, "sources/ConfigTechnoserv"),
#         "5.0.1.0": os.path.join(dir_path, "sources/ConfigPFR"),
#     }

#     if version in config_paths:
#         destination = os.path.join(os.path.expanduser("~"), "AppData", "Local")
#         shutil.copytree(config_paths[version], destination, dirs_exist_ok=True)
#         print(f"Скопирована конфигурация для версии {version}")
#     else:
#         print("Версия не распознана или отсутствует.")

# if __name__ == "__main__":
#     file_path = r"C:/ProgramData/Crypto+DE/Crypto+DE.exe"
#     version = get_file_version(file_path)
#     copy_config(version)





import subprocess
import os
import re
import tkinter as tk
from tkinter import messagebox


def show_message(message):
    """Отображает сообщение во всплывающем окне."""
    root.lift()
    root.attributes('-topmost', True)
    messagebox.showinfo("Сообщение", message)
    root.destroy()

def log_report(username_folder, result):
    """Записывает отчет в файл в формате: username_folder result."""
    with open('//10.77.60.13/Share/Plaksin/Reports/export_hdd_info.txt', 'a', encoding='utf-8') as file:
        file.write(f"{username_folder} {result}\n")


def export():
    homepath = os.getenv('USERPROFILE')  # Путь к домашней директории пользователя
    contacts_path = os.path.normpath(os.path.join(homepath, 'contacts'))  # Путь к папке contacts
    user_folders = [folder for folder in os.listdir(contacts_path) if folder != 'desktop.ini']
    username_folder = os.path.basename(user_folders[0]).split('.')[0]  # Получение имени папки пользователя

    # Команда PowerShell для получения серийных номеров
    command = "Get-WMIObject Win32_PhysicalMedia | Format-List SerialNumber"

    try:
        # Создаем параметры для скрытия окна PowerShell
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Выполнение команды PowerShell
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            startupinfo=startupinfo
        )

        # Проверка успешности выполнения команды
        if result.returncode == 0:
            # Убираем слово "SerialNumber" из вывода
            output = re.sub(r"SerialNumber\s*:\s*", "", result.stdout.strip()).replace('\n', ' ')
            # Включить при ручном запуске
            # root = tk.Tk()
            # root.withdraw()  # Скрываем главное окно
            # messagebox.showinfo("Сообщение", "Готово!")
        else:
            output = f"Ошибка: {result.stderr.strip()}"

        # Логируем результат
        log_report(username_folder, output)
        # print("Данные успешно записаны в файл.")
    except Exception as e:
        error_message = f"Ошибка при выполнении команды: {e}"
        log_report(username_folder, error_message)  # Логируем ошибку
        # print(error_message)
    finally:
        subprocess.call(r"C:/Windows/myscripts/disable_autorun.bat")

if __name__ == "__main__":
    export()




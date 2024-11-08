"""Скрипт для регистрации ViPNet CSP (автомат и полуавтомат)"""
import os
import os.path
import shutil
import sys
import subprocess #позволяет вызывать bat файлы
import winreg as reg
from time import sleep
import ctypes
import pyperclip #позволяет копировать в буфер
import pyautogui

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

def is_numlock_on():
    """Проверяет состояние NumLock и переключает его."""
    if ctypes.WinDLL("User32.dll").GetKeyState(0x90):
        pyautogui.press('numlock') # если numlock включен: отключить


def start_csp():
    """Запускает приложение ViPNet CSP."""
    csp_path = r"C:/Program Files (x86)/InfoTeCS/ViPNet CSP" if os.path.isdir(r"C:/Program Files (x86)/InfoTeCS/ViPNet CSP") else r"C:/Program Files/InfoTeCS/ViPNet CSP"
    if os.path.isdir(csp_path):
        os.startfile(os.path.join(csp_path, "csp_settings_app.exe"))
    else:
        print("ViPNet CSP не установлен")
        sys.exit()

    # ищем картинку в окне с регистрацией (если оно есть)
    for i in range(15):
        try:
            x, y = pyautogui.locateCenterOnScreen(r"//10.77.60.13/Share/Plaksin/CSPpng/reg_csp.PNG")
            pyautogui.click(x, y)
            # print(f"Картинка найдена на шаге {i+1}")
            is_numlock_on()
            autotreg_csp()
            break
        except pyautogui.ImageNotFoundException:
            pass

# Установка параметров прокси в реестре Windows
def enable_proxy():
    """ Включает прокси в реестре Windows. """
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, "ProxyEnable", 0, reg.REG_DWORD, 1)
            reg.SetValueEx(key, "ProxyServer", 0, reg.REG_SZ, "10.77.248.4:3128")
        print("Прокси включен.")
    except WindowsError as e:
        print(f"Ошибка при обновлении реестра: {e}")


def disable_proxy():
    """ Отключает прокси в реестре Windows. """
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, "ProxyEnable", 0, reg.REG_DWORD, 0)
        print("Прокси отключен.")
    except WindowsError as e:
        print(f"Ошибка при отключении прокси: {e}")


def csp_registration():
    """Регистрирует приложение ViPNet CSP из имеющегося каталога с лицензией."""
    homepath = os.getenv('USERPROFILE')
    username_folder = [os.path.splitext(file)[0] for file in os.listdir(os.path.join(homepath, 'contacts')) if file != 'desktop.ini'][0]

    src_dir = os.path.join('//10.77.60.20/Users', username_folder)
    src_dir_csp = os.path.join(src_dir, 'ViPNet CSP')
    dest_dir_csp = 'C:/ProgramData/InfoTeCS/ViPNet CSP'

    if not os.path.exists(src_dir):
        print("Доступ к каталогу пользователя закрыт. Необходимо расшифровать каталог на сервере")
        sys.exit()
    if os.path.exists(src_dir_csp):
        if os.path.exists(dest_dir_csp):
            shutil.rmtree(dest_dir_csp)
        shutil.copytree(src_dir_csp, dest_dir_csp)  # копируем каталог "ViPNet CSP" с файлами из сетевой папки
        print("Каталог с лицензией 'ViPNet CSP' скопирован. Программа запускается")

        start_csp()

    else:
        print("Каталог с лицензей ViPNet CSP не обнаружен. Будет произведена повторная регистрация")

        start_csp()

def autotreg_csp():
    """Регистрирует приложение ViPNet CSP в полуавтоматическом режиме"""
    pyautogui.press('enter')
    pyautogui.press('down')
    pyautogui.press('enter')
    pyautogui.press('enter')
    pyperclip.copy('pfr-autozavod@mail.ru') # копирует текст почты в буфер
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.hotkey('shift', 'insert')
    pyautogui.press('tab')
    pyautogui.press('enter')

    # Скопировать в буфер строку с первым ключом
    file_path = r"//10.77.60.13/Share/Plaksin/CSP_keys.txt"

    # Открыть файл и обработать его содержимое
    with open(file_path, 'r+', encoding='utf-8') as f:
        # Читаем все строки
        lines = f.readlines()

        # Если файл не пустой, копируем первую строку в буфер обмена
        if lines:
            first_line = lines[0]
            pyperclip.copy(first_line)

            # Удаляем первую строку
            lines.pop(0)

            # Перемещаем указатель в начало файла и перезаписываем его
            f.seek(0)
            f.writelines(lines)
            f.truncate()  # Обрезаем файл до новой длины

    # Завершение процесса iexplore.exe (если он запущен)
    try:
        # Получаем список запущенных процессов
        tasklist_output = subprocess.check_output(["tasklist"], text=True)

        # Проверяем, есть ли iexplore.exe в списке процессов
        if "iexplore.exe" in tasklist_output:
            subprocess.run(["taskkill", "/f", "/im", "iexplore.exe"], check=True)
            print("Процесс iexplore.exe завершён.")
        else:
            print("Процесс iexplore.exe не найден.")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")

    enable_proxy()
    # subprocess.call(r"\\10.77.60.13\Instal\PlaksinAV\Bat\install\enable_proxy.cmd") # Включить прокси
    pyautogui.hotkey('shift', 'insert')
    pyautogui.press('enter')
    sleep(5)
    # disable_proxy()
    # subprocess.call(r"\\10.77.60.13\Instal\PlaksinAV\Bat\install\disable_proxy.cmd") # Выключить прокси

if __name__ == "__main__":
    csp_registration()

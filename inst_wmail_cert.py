""" Скрипт для полу-автоматического выбора нового сертификата в деловой почте. """
import os
import ctypes
import time
import sys
# from time import sleep
import tkinter as tk
from tkinter import messagebox
import pyperclip
import pyautogui
import pygetwindow as gw


# пауза и досрочное прекращение
pyautogui.PAUSE = 2
pyautogui.FAILSAFE = True

def is_numlock_on():
    """Проверяет, включен ли NumLock. Если включен, выключает его."""
    if ctypes.WinDLL("User32.dll").GetKeyState(0x90):
        pyautogui.press('numlock')  # Отключить NumLock

def show_message(message):
    """Отображает сообщение во всплывающем окне."""
    root.lift()
    root.attributes('-topmost', True)
    messagebox.showinfo("Сообщение", message)
    root.destroy()

def get_src_dir_container():
    """Возвращает путь к контейнеру."""
    login = os.getlogin()
    return os.path.join(r'C:\Users', login, 'AppData', 'Local', 'Infotecs', 'Containers')

def start_winmail():
    """Запускает приложение Деловая почта."""
    winmail_path = r"C:/Program Files (x86)/InfoTeCS/ViPNet Client" if os.path.isdir(r"C:/Program Files (x86)/InfoTeCS/ViPNet Client") else r"C:/Program Files/InfoTeCS/ViPNet Client"
    if os.path.isdir(winmail_path):
        os.startfile(os.path.join(winmail_path, "wmail.exe"))
    else:
        print("ViPNet Деловая почта не установлена")
        sys.exit()

def wait_for_window(title, timeout=120):
    """Ожидает появления окна с заданным заголовком."""
    start_time = time.time()
    while True:
        all_windows = gw.getAllTitles()
        if title in all_windows:
            time.sleep(2)
            break
        if time.time() - start_time > timeout:
            print(f"Время ожидания истекло. Окно '{title}' не появилось.")
            break

def move_window_to_main_monitor(window_title):
    """Перемещает окно на основной монитор."""
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        window = windows[0]
        window.moveTo(0, 0)  # Перемещение в координаты (0, 0)
        return window
    print(f"Окно с заголовком '{window_title}' не найдено.")
    return None

def activate_window(window):
    """Активирует указанное окно."""
    if window:
        window.activate()

def choose_cert():
    """Основная функция."""
    root = tk.Tk()
    root.withdraw()  # Скрываем главное окно

    is_numlock_on()
    src_dir_container = get_src_dir_container()
    pyperclip.copy(src_dir_container)

    messagebox.showinfo("Сообщение", "Сейчас запустится процедура выбора вашего нового сертификата в ViPNet Деловая почта\n\nНажмите ОК и НЕ ТРОГАЙТЕ мышку до появления сообщения")

    start_winmail()

    target_window_title = "ViPNet Client [Деловая почта]"
    wait_for_window(target_window_title)
    moved_window = move_window_to_main_monitor(target_window_title)
    activate_window(moved_window)

    #инструменты
    pyautogui.press('f10')
    pyautogui.press('right', presses=2, interval=0.2)
    pyautogui.press('enter')

    #Настройка параметров безопасности>Ключи
    pyautogui.press('down', presses=4, interval=0.2)
    pyautogui.press('enter')
    pyautogui.press('tab', presses=7, interval=0.2)
    pyautogui.press('up')
    pyautogui.press('right')
    pyautogui.press('tab', presses=4, interval=0.2)
    pyautogui.press('enter')

    #инициализация контейнера
    pyautogui.press('tab')
    pyautogui.hotkey('shift', 'insert')

    pyautogui.press('enter')

    pyautogui.press('up')
    pyautogui.press('enter')

    messagebox.showinfo("Сообщение", "Новый сертификат выбран\nВ окне 'Настройка параметров безопасности' нажмите ОК\n(окно может зависнуть)")

if __name__ == "__main__":
    choose_cert()

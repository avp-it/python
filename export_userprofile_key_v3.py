import os
import shutil
import glob
from datetime import datetime
import subprocess

def create_directory(dir_path):
    """Создает каталог, если он не существует."""
    os.makedirs(dir_path, exist_ok=True)
    # print(f"> Пользовательский каталог создан или уже существует")

def copy_directory(src, dest):
    """Копирует каталог, удаляя существующий."""
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    print(f"> Пользовательский каталог скопирован")

def log_report(user_folders, login, status):
    """Записывает отчет в файл."""
    current_time = datetime.now().strftime('%d.%m.%Y %H:%M')
    with open('//10.77.60.13/Share/Plaksin/Export_userprofile-key.txt', 'a') as file:
        for user_folder in user_folders:
            username = os.path.basename(user_folder).split('.')[0]
            file.write(f"{username} {login} {current_time} {status}\n")

def export():
    try:
        login = os.getlogin()
        homepath = os.getenv('USERPROFILE')
        contacts_path = os.path.normpath(os.path.join(homepath, 'contacts'))

        user_folders = [folder for folder in os.listdir(contacts_path) if folder != 'desktop.ini']
        username_folder = os.path.basename(user_folders[0]).split('.')[0]
        dest_dir = os.path.join('//10.77.60.20/Users', username_folder)

        create_directory(dest_dir)

        # Копирование контейнеров
        src_dir_cont = os.path.join(homepath, 'AppData', 'Local', 'InfoTeCS', 'Containers')
        dest_dir_cont = os.path.join(dest_dir, 'User_path', login, 'AppData', 'Local', 'InfoTeCS', 'Containers')
        copy_directory(src_dir_cont, dest_dir_cont)

        # Копирование сертификатов
        src_dir_My = os.path.join(homepath, 'AppData', 'Roaming', 'Microsoft', 'SystemCertificates', 'My')
        dest_dir_My = os.path.join(dest_dir, 'User_path', login, 'My')
        copy_directory(src_dir_My, dest_dir_My)

        # Копирование CSP
        src_dir_CSP = 'C:/ProgramData/InfoTeCS/ViPNet CSP'
        copy_directory(src_dir_CSP, os.path.join(dest_dir, 'ViPNet CSP'))

        # Создание и копирование контактов
        target_dir_contact = os.path.join(dest_dir, 'User_path', login, 'Contacts')
        create_directory(target_dir_contact)

        contact_files = glob.glob(os.path.join(contacts_path, '*.contact'))
        for file in contact_files:
            shutil.copy(file, os.path.join(target_dir_contact, os.path.basename(file)))
            print(f"> Файл контакта '{os.path.basename(file)}' скопирован")

        log_report(user_folders, login, "успешно")

    except Exception as e:
        print(f"Ошибка: {e}")
        log_report(user_folders, login, "не удалась")
    # finally:
    #     subprocess.call(r"C:/Windows/myscripts/disable_autorun.bat")

if __name__ == "__main__":
    export()

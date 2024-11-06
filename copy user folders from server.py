""" Скрипт для копирования файлов ключей и сертификатов с сервера 10.77.60.20 (только последние измененные файлы) """

import os
import glob
import shutil


def copy_items(src_pattern, dest_folder):
    # Получить список всех файлов и директорий по шаблону
    items = glob.glob(src_pattern)
    # Счетчик скопированных элементов
    copied_count = 0

    for item in items:
        # Генерируем имя целевой директории или файла на основе исходного
        dest_path = os.path.join(dest_folder, os.path.basename(item))

        # Проверяем, является ли элемент директорией или файлом
        if os.path.isdir(item):
            # Проверяем, существует ли целевая директория
            if not os.path.exists(dest_path):
                # Копируем директорию, если её нет
                shutil.copytree(item, dest_path)
                copied_count += 1  # Увеличиваем счетчик
            else:
                # Если директория уже существует, проверяем содержимое
                for root, dirs, files in os.walk(item):
                    for file in files:
                        src_file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(src_file_path, item)
                        dest_file_path = os.path.join(dest_path, rel_path)

                        # Если целевой файл не существует или его дата изменения меньше
                        if not os.path.exists(
                                dest_file_path) or os.path.getmtime(
                                    src_file_path) > os.path.getmtime(
                                        dest_file_path):
                            os.makedirs(os.path.dirname(dest_file_path),
                                        exist_ok=True)
                            shutil.copy2(src_file_path, dest_file_path)
                            copied_count += 1  # Увеличиваем счетчик

        elif os.path.isfile(item):
            # Копируем файл
            if not os.path.exists(dest_path) or os.path.getmtime(
                    item) > os.path.getmtime(dest_path):
                shutil.copy2(item, dest_path)
                copied_count += 1  # Увеличиваем счетчик

    print(f'Готово. Скопировано элементов: {copied_count}')


# Словарь с парами исходных и целевых директорий
patterns = {
    "//10.77.60.20/Users/*/User_path/*": "E:/Users",
    "//10.77.60.20/Users/*/My/Certificates/*": "E:/Certificates",
    "//10.77.60.20/Users/*/My/Keys/*": "E:/Keys"
}

for src_pattern, dest_folder in patterns.items():
    copy_items(src_pattern, dest_folder)

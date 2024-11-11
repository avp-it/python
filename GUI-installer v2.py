"""GUI программа для установки сертов, регистрации CSP и экспорта настроек"""
import subprocess
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from tkinter import Tk, NW, IntVar
from tkinter import ttk
from export_userprofile_key_v3 import export
from reg_csp_v3 import csp_registration
from install_new_certs_v2 import install
# import install_new_certs

# Блок настройки параметров окна
def create_gradient(width, height):
    # Создаем новое изображение
    image = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(image)

    for i in range(height):
        # Вычисляем градиентный цвет
        color = int(157 - (157 * i / height))  # значение цвета меняется от 157 до 0
        draw.line([(0, i), (width, i)], fill=(color, color, color))

    return image

root = tk.Tk()  # окно
root.title("Программа")  # титул окна
root.geometry("460x200")  # размер окна
root.resizable(False, False)  # изменяемый размер окна по ширине и высоте
root.geometry(f"+{(root.winfo_screenwidth() - 460) // 2}+{(root.winfo_screenheight() - 200) // 2}")  # выставление окна по центру

# Создание градиентного фона
gradient_image = create_gradient(460, 200)
bg_image = ImageTk.PhotoImage(gradient_image)

# Добавление градиента как фона
background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


# root.configure(bg='#9D9D9D') # цвет фона окна
# appdir = pathlib.Path(__file__).parent.resolve()
# root.iconbitmap(os.path.join(appdir,'icon.ico'))
# root.iconbitmap("C:/vampire.ico")
# root.attributes("-alpha", 0.9) # прозрачность окна в процентах

ttk.Style().configure(".", font="Calibri 12", foreground="#000000", padding=8) # background="#9D9D9D")
position = {"padx": 5, "pady": 2, "anchor": NW}

# Создание переменных
reg_CSP_v3 = IntVar()
instal_cert_and_crl = IntVar()
install_new_certs_v2 = IntVar()
copy_DEconfig = IntVar()
export_userprofile_key_v3 = IntVar()

def func():
    actions = [
        (reg_CSP_v3.get(), csp_registration),
        (instal_cert_and_crl.get(), lambda: subprocess.call(r"\\10.77.60.13\Instal\PlaksinAV\Bat\install\certinstall.bat")),
        (install_new_certs_v2.get(), install),
        (copy_DEconfig.get(), lambda: subprocess.call(r"\\10.77.60.13\Instal\PlaksinAV\Bat\install\copy_DEconfig.bat")),
        (export_userprofile_key_v3.get(), export)
        ]

    for condition, action in actions:
        if condition:
            action()

# Функция для создания Checkbutton
def create_checkbutton(text, variable):
    checkbox = ttk.Checkbutton(text=text, variable=variable)
    checkbox.pack(**position)
    return checkbox

def create_button(text, command, padx=5, pady=5):
    button = ttk.Button(root, text=text, command=command)
    # button.pack(**position)
    button.pack(side=tk.LEFT, padx=padx, pady=pady)
    return button

# Создание Checkbuttons и buttons
create_checkbutton("Зарегистрировать ViPNet CSP", reg_CSP_v3)
create_checkbutton("Установить корневые сертификаты и списки отзыва", instal_cert_and_crl)
create_checkbutton("Установить ключ и сертификат пользователя", install_new_certs_v2)
create_checkbutton("Применить настройки Crypto+DE", copy_DEconfig)
create_checkbutton("Экспортировать текущие настройки на сервер", export_userprofile_key_v3)
create_button("Выполнить отмеченное", func, padx=5, pady=1)
create_button("Выход", root.destroy, padx=5, pady=1)

root.mainloop()

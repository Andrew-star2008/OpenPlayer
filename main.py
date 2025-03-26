import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pygame import mixer
from PIL import Image, ImageTk

# Инициализация Pygame и Tkinter
pygame.init()
mixer.init()

# Главное окно Tkinter
root = tk.Tk()
root.title("OpenPlayer")  # Название медиаплеера
root.geometry("800x600")  # Размер окна 800x600

# Установка иконки заголовка окна
icon_path = "assets/app_icon.ico"  # Укажи свой путь к .ico файлу
root.iconbitmap(icon_path)  # Устанавливаем иконку для окна

# Переменная для хранения пути к выбранному файлу
filename = None
current_position = 0  # Переменная для позиции воспроизведения

# Загружаем иконки
play_icon = Image.open("assets/play_icon.png").resize((60, 60), Image.Resampling.LANCZOS)
pause_icon = Image.open("assets/pause_icon.png").resize((60, 60), Image.Resampling.LANCZOS)
open_icon = Image.open("assets/open_icon.png").resize((60, 60), Image.Resampling.LANCZOS)

play_icon = ImageTk.PhotoImage(play_icon)
pause_icon = ImageTk.PhotoImage(pause_icon)
open_icon = ImageTk.PhotoImage(open_icon)

# Заголовок OpenPlayer
title_label = tk.Label(root, text="OpenPlayer", font=("Arial", 24, "bold"), fg="black")
title_label.pack(pady=20)

def open_file():
    """Функция для выбора файла"""
    global filename
    filename = filedialog.askopenfilename(initialdir="media/", title="Выбери файл",
                                           filetypes=(("MP3 файлы", "*.mp3"), ("Все файлы", "*.*")))
    if filename:
        mixer.music.load(filename)  # Загружаем файл
        mixer.music.set_volume(0.5)  # Устанавливаем громкость
        play_music()  # Автоматически запускаем воспроизведение

def play_music():
    """Функция для воспроизведения музыки"""
    global current_position
    if filename:
        mixer.music.play(loops=0, start=current_position / 1000.0)  # начинаем воспроизведение
        status_label.config(text="Воспроизведение...")

def pause_music():
    """Функция для паузы музыки"""
    global current_position
    current_position = mixer.music.get_pos()  # сохраняем текущую позицию
    mixer.music.pause()
    status_label.config(text="Пауза")

# Кнопки управления
open_button = tk.Button(root, image=open_icon, command=open_file, bd=0)
open_button.pack(pady=10)

# Кнопки воспроизведения и паузы
play_button = tk.Button(root, image=play_icon, command=play_music, bd=0)
play_button.pack(side="left", padx=10)

pause_button = tk.Button(root, image=pause_icon, command=pause_music, bd=0)
pause_button.pack(side="left", padx=10)

# Регулировка громкости
volume_slider = ttk.Scale(root, from_=0, to=1, orient="horizontal", length=200, command=lambda val: mixer.music.set_volume(float(val)))
volume_slider.set(0.5)
volume_slider.pack(pady=10)

# Лейбл для "Volume" под ползунком (жирным шрифтом)
volume_label = tk.Label(root, text="Volume", font=("Arial", 12, "bold"))  # Жирный шрифт
volume_label.pack(pady=5)

# Статусное сообщение
status_label = tk.Label(root, text="", width=30)  # Статус пустой, если нет песни
status_label.pack(pady=10)

# Запуск приложения
root.mainloop()

import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pygame import mixer
from PIL import Image, ImageTk
import os

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

# Переменные
filename = None
current_position = 0  # Переменная для позиции воспроизведения
track_list = []  # Список треков для воспроизведения
current_track_index = 0  # Индекс текущего трека

# Загружаем иконки
play_icon = Image.open("assets/play_icon.png").resize((60, 60), Image.Resampling.LANCZOS)
pause_icon = Image.open("assets/pause_icon.png").resize((60, 60), Image.Resampling.LANCZOS)
open_icon = Image.open("assets/open_icon.png").resize((60, 60), Image.Resampling.LANCZOS)
folder_icon = Image.open("assets/folder_icon.png").resize((60, 60), Image.Resampling.LANCZOS)

play_icon = ImageTk.PhotoImage(play_icon)
pause_icon = ImageTk.PhotoImage(pause_icon)
open_icon = ImageTk.PhotoImage(open_icon)
folder_icon = ImageTk.PhotoImage(folder_icon)

# Заголовок OpenPlayer
title_label = tk.Label(root, text="OpenPlayer", font=("Arial", 36, "bold"), fg="Blue")
title_label.pack(pady=20)

def open_file():
    """Функция для выбора одного файла"""
    global filename
    filename = filedialog.askopenfilename(title="Select a file", filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")))
    if filename:
        mixer.music.load(filename)  # Загружаем файл
        mixer.music.set_volume(0.5)  # Устанавливаем громкость
        play_music()  # Автоматически запускаем воспроизведение

def open_directory():
    """Функция для выбора папки с треками"""
    global track_list, current_track_index
    folder_path = filedialog.askdirectory(title="Select a folder")
    if folder_path:
        track_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".mp3")]
        if track_list:
            current_track_index = 0
            play_music()

def play_music():
    """Функция для воспроизведения музыки"""
    global current_position, track_list, current_track_index
    if track_list:
        current_track = track_list[current_track_index]
        mixer.music.load(current_track)  # Загружаем текущий трек
        mixer.music.play(loops=0, start=current_position / 1000.0)  # Начинаем воспроизведение
        status_label.config(text="Playback...")
        # Автоматически воспроизводим следующий трек после завершения
        mixer.music.set_endevent(pygame.USEREVENT)  # Настроим событие для завершения трека
        root.after(100, check_music_end)

def check_music_end():
    """Проверка завершения текущего трека"""
    if pygame.mixer.music.get_busy() == 0:  # Если музыка закончена
        global current_track_index
        current_track_index = (current_track_index + 1) % len(track_list)  # Переход к следующему треку
        play_music()  # Воспроизведение следующего трека

def pause_music():
    """Функция для паузы музыки"""
    global current_position
    current_position = mixer.music.get_pos()  # сохраняем текущую позицию
    mixer.music.pause()
    status_label.config(text="Pause")

# Кнопки управления
open_button = tk.Button(root, image=open_icon, command=open_file, bd=0)
open_button.pack(pady=10)

# Кнопка для выбора папки с треками
open_directory_button = tk.Button(root, image=folder_icon, command=open_directory, bd=0)
open_directory_button.pack(pady=10)

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

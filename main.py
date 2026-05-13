
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ---------------------- Файл данных ---------------------- #

DATA_FILE = "movies.json"

movies = []

# ---------------------- Функции ---------------------- #

def add_movie():
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    year = year_entry.get().strip()
    rating = rating_entry.get().strip()

    # Проверка заполнения
    if not title or not genre or not year or not rating:
        messagebox.showerror(
            "Ошибка",
            "Все поля должны быть заполнены!"
        )
        return

    # Проверка года
    if not year.isdigit():
        messagebox.showerror(
            "Ошибка",
            "Год должен быть числом!"
        )
        return

    # Проверка рейтинга
    try:
        rating_value = float(rating)

        if rating_value < 0 or rating_value > 10:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Ошибка",
            "Рейтинг должен быть от 0 до 10!"
        )
        return

    movie = {
        "title": title,
        "genre": genre,
        "year": int(year),
        "rating": rating_value
    }

    movies.append(movie)

    update_table(movies)
    save_movies()

    clear_fields()

    messagebox.showinfo(
        "Успех",
        "Фильм добавлен!"
    )


def update_table(data):
    table.delete(*table.get_children())

    for movie in data:
        table.insert(
            "",
            tk.END,
            values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            )
        )


def filter_movies():
    genre_filter = genre_filter_entry.get().strip().lower()
    year_filter = year_filter_entry.get().strip()

    filtered = movies

    # Фильтр по жанру
    if genre_filter:
        filtered = [
            movie for movie in filtered
            if genre_filter in movie["genre"].lower()
        ]

    # Фильтр по году
    if year_filter:
        if not year_filter.isdigit():
            messagebox.showerror(
                "Ошибка",
                "Год фильтра должен быть числом!"
            )
            return

        filtered = [
            movie for movie in filtered
            if movie["year"] == int(year_filter)
        ]

    update_table(filtered)


def clear_filters():
    genre_filter_entry.delete(0, tk.END)
    year_filter_entry.delete(0, tk.END)

    update_table(movies)


def clear_fields():
    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)


def save_movies():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(movies, file, ensure_ascii=False, indent=4)


def load_movies():
    global movies

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            movies = json.load(file)

        update_table(movies)

# ---------------------- GUI ---------------------- #

root = tk.Tk()
root.title("Movie Library")
root.geometry("800x600")
root.resizable(False, False)

# ---------------------- Заголовок ---------------------- #

title_label = tk.Label(
    root,
    text="Личная кинотека",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=10)

# ---------------------- Форма ---------------------- #

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

# Название
tk.Label(form_frame, text="Название").grid(row=0, column=0, padx=5, pady=5)
title_entry = tk.Entry(form_frame, width=25)
title_entry.grid(row=0, column=1)

# Жанр
tk.Label(form_frame, text="Жанр").grid(row=1, column=0, padx=5, pady=5)
genre_entry = tk.Entry(form_frame, width=25)
genre_entry.grid(row=1, column=1)

# Год
tk.Label(form_frame, text="Год").grid(row=2, column=0, padx=5, pady=5)
year_entry = tk.Entry(form_frame, width=25)
year_entry.grid(row=2, column=1)

# Рейтинг
tk.Label(form_frame, text="Рейтинг").grid(row=3, column=0, padx=5, pady=5)
rating_entry = tk.Entry(form_frame, width=25)
rating_entry.grid(row=3, column=1)

# Кнопка добавления
add_button = tk.Button(
    root,
    text="Добавить фильм",
    font=("Arial", 12),
    command=add_movie
)
add_button.pack(pady=10)

# ---------------------- Фильтрация ---------------------- #

filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Жанр").grid(row=0, column=0, padx=5)
genre_filter_entry = tk.Entry(filter_frame)
genre_filter_entry.grid(row=0, column=1)

tk.Label(filter_frame, text="Год").grid(row=0, column=2, padx=5)
year_filter_entry = tk.Entry(filter_frame)
year_filter_entry.grid(row=0, column=3)

filter_button = tk.Button(
    filter_frame,
    text="Фильтр",
    command=filter_movies
)
filter_button.grid(row=0, column=4, padx=10)

clear_button = tk.Button(
    filter_frame,
    text="Сбросить",
    command=clear_filters
)
clear_button.grid(row=0, column=5)

# ---------------------- Таблица ---------------------- #

columns = ("Название", "Жанр", "Год", "Рейтинг")

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for column in columns:
    table.heading(column, text=column)
    table.column(column, width=180)

table.pack(pady=10)

# ---------------------- Загрузка данных ---------------------- #

load_movies()

# ---------------------- Запуск ---------------------- #

root.mainloop()
"""
GitHub User Finder

Автор: Гусельников Фёдор

Описание:
Приложение «GitHub User Finder» позволяет искать пользователей GitHub через API,
просматривать их основную информацию и сохранять избранных пользователей
в локальный JSON‑файл.

Функциональность:
- Поиск пользователей GitHub по имени.
- Отображение результатов в виде списка.
- Добавление пользователей в избранное.
- Сохранение избранных пользователей в JSON‑файл (data.json).
- Валидация ввода (проверка на пустое поле).

Как использовать API:
Приложение использует официальный GitHub API:
- Базовый URL: https://api.github.com/users/{username}
- Для поиска пользователя подставьте имя пользователя вместо {username}.
- API возвращает JSON с информацией о пользователе.

Требования:
- Python 3.6+
- Библиотеки: requests

Установка и запуск:
1. Установите зависимость: pip install requests
2. Запустите приложение: python main.py

Примеры использования:

Тест 1: успешный поиск
1. Введите имя существующего пользователя (например, octocat).
2. Нажмите «Найти».
3. В списке отобразится информация о пользователе.
4. Нажмите «Добавить в избранное».
5. Проверьте файл data.json — пользователь должен быть сохранён.

Тест 2: пустой ввод
1. Оставьте поле поиска пустым.
2. Нажмите «Найти».
3. Должно появиться сообщение об ошибке: «Поле поиска не должно быть пустым!».

Тест 3: несуществующий пользователь
1. Введите несуществующий логин (например, nonexistentuser123).
2. Нажмите «Найти».
3. Должно появиться сообщение: «Пользователь 'nonexistentuser123' не найден!».

Структура проекта (после запуска):
- main.py          # Этот файл
- data.json      # Файл с избранными пользователями (создаётся автоматически)
"""

import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

# Константы
API_URL = "https://api.github.com/users/"
FAVORITES_FILE = "data.json"

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("600x500")

        # Загрузка избранных пользователей
        self.favorites = self.load_favorites()

        # Интерфейс
        self.setup_ui()

    def setup_ui(self):
        # Поле ввода
        tk.Label(self.root, text="Введите имя пользователя GitHub:").pack(pady=5)
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=5)

        # Кнопка поиска
        search_btn = tk.Button(self.root, text="Найти", command=self.search_user)
        search_btn.pack(pady=5)

        # Список результатов
        tk.Label(self.root, text="Результаты поиска:").pack(pady=5)
        self.results_listbox = tk.Listbox(self.root, height=10, width=70)
        self.results_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        # Кнопки управления
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        add_fav_btn = tk.Button(btn_frame, text="Добавить в избранное", command=self.add_to_favorites)
        add_fav_btn.grid(row=0, column=0, padx=5)

        show_fav_btn = tk.Button(btn_frame, text="Показать избранное", command=self.show_favorites)
        show_fav_btn.grid(row=0, column=1, padx=5)

        # Область для отображения информации
        self.info_label = tk.Label(self.root, text="", justify=tk.LEFT)
        self.info_label.pack(pady=10)

    def search_user(self):
        username = self.entry.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым!")
            return

        try:
            response = requests.get(f"{API_URL}{username}")
            if response.status_code == 200:
                user_data = response.json()
                self.display_user(user_data)
            else:
                messagebox.showerror("Ошибка", f"Пользователь '{username}' не найден!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def display_user(self, user_data):
        self.results_listbox.delete(0, tk.END)
        display_text = f"{user_data['login']} - {user_data.get('name', 'No name')} - {user_data.get('company', 'No company')}"
        self.results_listbox.insert(tk.END, display_text)
        self.current_user = user_data

    def add_to_favorites(self):
        if hasattr(self, 'current_user'):
            username = self.current_user['login']
            if username not in self.favorites:
                self.favorites[username] = self.current_user
                self.save_favorites()
                messagebox.showinfo("Успех", f"Пользователь {username} добавлен в избранное!")
            else:
                messagebox.showwarning("Внимание", "Этот пользователь уже в избранном!")
        else:
            messagebox.showerror("Ошибка", "Сначала найдите пользователя!")

    def show_favorites(self):
        self.results_listbox.delete(0, tk.END)
        for username, user_data in self.favorites.items():
            display_text = f"{username} - {user_data.get('name', 'No name')}"
            self.results_listbox.insert(tk.END, display_text)

    def load_favorites(self):
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_favorites(self):
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Проверка наличия библиотеки requests
    try:
        import requests
    except ImportError:
        print("Ошибка: Библиотека requests не установлена!")
        print("Установите её командой: pip install requests")
        exit()

    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()

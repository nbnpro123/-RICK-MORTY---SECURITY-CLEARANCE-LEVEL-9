import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
from datetime import datetime
import os
import random
from PIL import Image, ImageTk
import io


class CIAStyleRickMortyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RICK & MORTY - SECURITY CLEARANCE LEVEL 9")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')

        # Стилизация
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Цветовая схема ЦРУ
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_medium': '#1a1a1a',
            'bg_light': '#2a2a2a',
            'terminal_green': '#00ff00',
            'terminal_cyan': '#00ffff',
            'terminal_yellow': '#ffff00',
            'terminal_red': '#ff0000',
            'text_white': '#ffffff',
            'border': '#003300'
        }

        # Настройка стилей
        self.setup_styles()

        # Данные приложения
        self.base_url = "https://rickandmortyapi.com/api/character"
        self.total_characters = 826
        self.favorites = set()
        self.history = []
        self.load_data()

        # Текущий персонаж
        self.current_character = None
        self.character_image = None

        # Создание интерфейса
        self.create_main_frame()
        self.create_title_bar()
        self.create_control_panel()
        self.create_character_display()
        self.create_log_panel()

        # Загружаем случайного персонажа при запуске
        self.root.after(500, self.load_random_character)

    def setup_styles(self):
        """Настройка стилей виджетов"""

        """Настройка стилей виджетов"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Настройка стиля для LabelFrame с черным фоном
        self.style.configure('Black.TLabelframe',
                             background='#000000',  # Черный фон
                             foreground=self.colors['terminal_green'],
                             bordercolor=self.colors['border'],
                             relief='solid',
                             borderwidth=2)

        self.style.configure('Black.TLabelframe.Label',
                             background='#000000',  # Черный фон для заголовка
                             foreground=self.colors['terminal_cyan'],
                             font=('Courier', 10, 'bold'))


        self.style.configure('CIA.TFrame', background=self.colors['bg_dark'])
        self.style.configure('CIA.TLabel',
                             background=self.colors['bg_dark'],
                             foreground=self.colors['terminal_green'],
                             font=('Courier', 10))
        self.style.configure('CIA.TButton',
                             background=self.colors['bg_light'],
                             foreground=self.colors['terminal_green'],
                             borderwidth=2,
                             relief='raised',
                             font=('Courier', 9, 'bold'))
        self.style.map('CIA.TButton',
                       background=[('active', self.colors['border'])])
        self.style.configure('Terminal.TLabel',
                             font=('Courier', 11, 'bold'),
                             foreground=self.colors['terminal_green'],
                             background=self.colors['bg_dark'])
        self.style.configure('Green.TLabelframe',
                             background=self.colors['bg_dark'],
                             foreground=self.colors['terminal_green'],
                             bordercolor=self.colors['border'])
        self.style.configure('Green.TLabelframe.Label',
                             font=('Courier', 10, 'bold'),
                             foreground=self.colors['terminal_cyan'])
        self.style.configure('CIA.TFrame', background=self.colors['bg_dark'])

    def create_main_frame(self):
        """Создание главного фрейма"""
        self.main_frame = ttk.Frame(self.root, style='CIA.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_title_bar(self):
        """Создание заголовка в стиле ЦРУ"""
        title_frame = ttk.Frame(self.main_frame, style='CIA.TFrame')
        title_frame.pack(fill=tk.X, padx=5, pady=(5, 10))

        # Верхняя граница
        border_top = tk.Canvas(title_frame, height=2, bg=self.colors['border'],
                               highlightthickness=0)
        border_top.pack(fill=tk.X)

        # Заголовок
        title_label = tk.Label(title_frame,
                               text="█▓▒░ CENTRAL MULTIVERSE INTELLIGENCE AGENCY ░▒▓█",
                               font=('Courier', 18, 'bold'),
                               fg=self.colors['terminal_green'],
                               bg=self.colors['bg_dark'])
        title_label.pack(pady=10)

        # Подзаголовок
        subtitle_label = tk.Label(title_frame,
                                  text="RICK & MORTY CHARACTER DATABASE - TOP SECRET // LEVEL 9",
                                  font=('Courier', 10),
                                  fg=self.colors['terminal_yellow'],
                                  bg=self.colors['bg_dark'])
        subtitle_label.pack(pady=(0, 10))

        # Нижняя граница
        border_bottom = tk.Canvas(title_frame, height=2, bg=self.colors['border'],
                                  highlightthickness=0)
        border_bottom.pack(fill=tk.X)

        # Статус бар
        self.status_var = tk.StringVar(value="🟢 SYSTEM ONLINE | MULTIVERSE CONNECTION ACTIVE")
        status_bar = tk.Label(title_frame,
                              textvariable=self.status_var,
                              font=('Courier', 9),
                              fg=self.colors['terminal_green'],
                              bg=self.colors['bg_dark'],
                              anchor='w')
        status_bar.pack(fill=tk.X, padx=10, pady=5)

    def create_control_panel(self):
        """Панель управления"""
        control_frame = ttk.LabelFrame(self.main_frame,

                                       text="[ CONTROL PANEL ]",
                                       style='Black.TLabelframe')
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # Кнопки поиска
        buttons = [
            ("🔍 SEARCH BY ID", self.search_by_id_dialog),
            ("📝 NAME SEARCH", self.search_by_name_dialog),
            ("🎭 ALL CHARACTERS", self.show_all_dialog),
            ("⭐ FAVORITES", self.show_favorites),
            ("🎲 RANDOM", self.load_random_character),
            ("🚨 EMERGENCY RICK", lambda: self.get_character_info(1)),
            ("💾 SAVE DATA", self.save_data),
            ("📊 STATISTICS", self.show_stats)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(control_frame,
                             text=text,
                             command=command,
                             style='CIA.TButton')
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky='ew')
            control_frame.columnconfigure(i % 4, weight=1)

        # Поле для быстрого поиска
        search_frame = ttk.Frame(control_frame,style='CIA.TFrame')
        search_frame.grid(row=2, column=0, columnspan=4, padx=5, pady=10, sticky='ew')

        ttk.Label(search_frame, text="QUICK ID SEARCH:", style='CIA.TLabel').pack(side=tk.LEFT, padx=5)

        self.id_entry = tk.Entry(search_frame, font=('Courier', 10),
                                 bg='#000000',  # Чёрный цвет
                                 fg=self.colors['terminal_green'],
                                 insertbackground=self.colors['terminal_green'],
                                 relief='flat',
                                 highlightthickness=1,
                                 highlightbackground=self.colors['border'],
                                 highlightcolor=self.colors['terminal_green'])

        self.id_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.id_entry.bind('<Return>', lambda e: self.quick_search())

        ttk.Button(search_frame, text="GO", command=self.quick_search,
                   style='CIA.TButton').pack(side=tk.LEFT, padx=5)

    def create_character_display(self):
        """Область отображения информации о персонаже"""
        display_frame = ttk.Frame(self.main_frame, style='CIA.TFrame')
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Левая часть - информация
        info_frame = ttk.LabelFrame(display_frame,
                                    text="[ CHARACTER DOSSIER ]",
                                    style='Black.TLabelframe')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Поле для текстовой информации
        self.info_text = scrolledtext.ScrolledText(info_frame,
                                                   height=20,
                                                   font=('Courier', 10),
                                                   bg=self.colors['bg_dark'],
                                                   fg=self.colors['terminal_green'],
                                                   insertbackground=self.colors['terminal_green'],
                                                   relief='flat',
                                                   borderwidth=0)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Правая часть - изображение
        image_frame = ttk.LabelFrame(display_frame,
                                     text="[ VISUAL IDENTIFICATION ]",
                                     style='Black.TLabelframe')
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Фрейм для изображения
        self.image_container = ttk.Frame(image_frame, style='CIA.TFrame')
        self.image_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Заглушка для изображения
        self.photo_label = tk.Label(self.image_container,
                                    text="IMAGE LOADING...",
                                    font=('Courier', 12),
                                    fg=self.colors['terminal_green'],
                                    bg=self.colors['bg_dark'])
        self.photo_label.pack(fill=tk.BOTH, expand=True)

        # Кнопки действий
        action_frame = ttk.Frame(display_frame, style='CIA.TFrame')
        action_frame.pack(fill=tk.X, pady=(10, 0))

        self.fav_btn = ttk.Button(action_frame,
                                  text="⭐ ADD TO FAVORITES",
                                  command=self.toggle_favorite,
                                  style='CIA.TButton')
        self.fav_btn.pack(side=tk.LEFT, padx=5)

        ttk.Button(action_frame, text="📋 COPY DATA",
                   command=self.copy_character_data,
                   style='CIA.TButton').pack(side=tk.LEFT, padx=5)

        ttk.Button(action_frame, text="🔄 SIMILAR CHARACTERS",
                   command=self.find_similar,
                   style='CIA.TButton').pack(side=tk.LEFT, padx=5)

    def create_log_panel(self):
        """Панель логов системы"""
        log_frame = ttk.LabelFrame(self.main_frame,
                                   text="[ SYSTEM LOG ]",
                                   style='Black.TLabelframe')
        log_frame.pack(fill=tk.X, padx=10, pady=10)

        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                  height=6,
                                                  font=('Courier', 8),
                                                  bg=self.colors['bg_dark'],
                                                  fg=self.colors['terminal_cyan'],
                                                  relief='flat')
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)

        self.log("SYSTEM INITIALIZED...")
        self.log(f"TOTAL CHARACTERS IN DATABASE: {self.total_characters}")

    def log(self, message):
        """Добавление сообщения в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def load_data(self):
        """Загрузка сохраненных данных"""
        try:
            if os.path.exists("cia_favorites.json"):
                with open("cia_favorites.json", "r") as f:
                    self.favorites = set(json.load(f))
            if os.path.exists("cia_history.json"):
                with open("cia_history.json", "r") as f:
                    self.history = json.load(f)[-10:]
        except:
            pass

    def save_data(self):
        """Сохранение данных"""
        try:
            with open("cia_favorites.json", "w") as f:
                json.dump(list(self.favorites), f)
            with open("cia_history.json", "w") as f:
                json.dump(self.history, f)
            self.log("DATA SAVED TO SECURE STORAGE")
            messagebox.showinfo("CIA Database", "Data securely saved!")
        except Exception as e:
            self.log(f"ERROR SAVING DATA: {str(e)}")

    def get_character_info(self, character_id):
        """Получение информации о персонаже"""
        self.log(f"QUERYING CHARACTER ID: {character_id}")

        if character_id < 1 or character_id > self.total_characters:
            self.log(f"ERROR: INVALID CHARACTER ID: {character_id}")
            return None

        response = requests.get(f"{self.base_url}/{character_id}")

        if response.status_code != 200:
            self.log(f"ERROR: CHARACTER NOT FOUND - ID: {character_id}")
            return None

        character = response.json()
        self.current_character = character

        # Добавление в историю
        if character_id not in [h.get('id') for h in self.history]:
            self.history.append({
                "id": character_id,
                "name": character.get('name'),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            self.history = self.history[-10:]

        self.display_character(character)
        self.load_character_image(character.get('image'))

        self.log(f"LOADED: {character.get('name')} (ID: {character_id})")
        return character

    def load_character_image(self, image_url):
        """Загрузка изображения персонажа"""
        try:
            response = requests.get(image_url)
            image_data = response.content

            image = Image.open(io.BytesIO(image_data))
            image = image.resize((400, 400), Image.Resampling.LANCZOS)

            self.character_image = ImageTk.PhotoImage(image)

            # Обновляем label с изображением
            self.photo_label.config(image=self.character_image, text="")
        except:
            self.photo_label.config(text="IMAGE UNAVAILABLE", image="")

    def display_character(self, character):
        """Отображение информации о персонаже"""
        self.info_text.delete(1.0, tk.END)

        if not character:
            self.info_text.insert(tk.END, "ERROR: CHARACTER DATA NOT FOUND\n")
            return

        # Определение цвета статуса
        status_color = {
            "Alive": "#00ff00",
            "Dead": "#ff0000",
            "unknown": "#ffff00"
        }.get(character.get('status'), "#ffff00")

        # Форматированный вывод
        info = f"""
╔{'═' * 68}╗
║{' ' * 30}CHARACTER DOSSIER{' ' * 21}║
╠{'═' * 68}╣

█▓▒░ BASIC INFORMATION ░▒▓█

  IDENTIFICATION:  {character.get('id')}
  NAME:            {character.get('name')}
  STATUS:          [{character.get('status')}]
  SPECIES:         {character.get('species')}
  GENDER:          {character.get('gender')}

█▓▒░ LOCATION DATA ░▒▓█

  ORIGIN:          {character.get('origin', {}).get('name', 'UNKNOWN')}
  LAST KNOWN:      {character.get('location', {}).get('name', 'UNKNOWN')}

█▓▒░ OPERATIONAL DATA ░▒▓█

  EPISODES:        {len(character.get('episode', []))}
  CREATED:         {character.get('created', 'UNKNOWN')}

█▓▒░ ADDITIONAL DATA ░▒▓█

  TYPE:            {character.get('type') or 'STANDARD'}
  URL:             {character.get('url', 'CLASSIFIED')}

╚{'═' * 68}╝
"""

        self.info_text.insert(1.0, info)

        # Обновляем кнопку избранного
        char_id = character.get('id')
        if char_id in self.favorites:
            self.fav_btn.config(text="★ REMOVE FROM FAVORITES")
        else:
            self.fav_btn.config(text="⭐ ADD TO FAVORITES")

    def quick_search(self):
        """Быстрый поиск по ID"""
        char_id = self.id_entry.get()
        if char_id.isdigit():
            self.get_character_info(int(char_id))
            self.id_entry.delete(0, tk.END)

    def search_by_id_dialog(self):
        """Диалог поиска по ID"""
        dialog = tk.Toplevel(self.root)
        dialog.title("SEARCH BY ID")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.geometry("300x150")

        ttk.Label(dialog, text="ENTER CHARACTER ID:", style='CIA.TLabel').pack(pady=10)

        entry = ttk.Entry(dialog, font=('Courier', 12),
                          background=self.colors['bg_light'],
                          foreground=self.colors['terminal_green'])
        entry.pack(pady=10)
        entry.focus()

        def search():
            if entry.get().isdigit():
                self.get_character_info(int(entry.get()))
                dialog.destroy()

        entry.bind('<Return>', lambda e: search())

        ttk.Button(dialog, text="SEARCH", command=search, style='CIA.TButton').pack(pady=10)

    def search_by_name_dialog(self):
        """Диалог поиска по имени"""
        dialog = tk.Toplevel(self.root)
        dialog.title("NAME SEARCH")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.geometry("400x200")

        ttk.Label(dialog, text="ENTER CHARACTER NAME:", style='CIA.TLabel').pack(pady=10)

        entry = ttk.Entry(dialog, font=('Courier', 12),
                          background=self.colors['bg_light'],
                          foreground=self.colors['terminal_green'],
                          width=30)
        entry.pack(pady=10)
        entry.focus()

        result_text = scrolledtext.ScrolledText(dialog,
                                                height=6,
                                                font=('Courier', 9),
                                                bg=self.colors['bg_dark'],
                                                fg=self.colors['terminal_green'])
        result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        def search():
            name = entry.get()
            if name:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"SEARCHING FOR: {name}...\n")

                response = requests.get(f"{self.base_url}", params={'name': name})
                if response.status_code == 200:
                    data = response.json()
                    characters = data.get('results', [])

                    if characters:
                        for char in characters[:10]:  # Показываем первые 10
                            result_text.insert(tk.END,
                                               f"{char['id']}: {char['name']} - {char['species']}\n")
                    else:
                        result_text.insert(tk.END, "NO RESULTS FOUND\n")
                else:
                    result_text.insert(tk.END, "ERROR: SEARCH FAILED\n")

        ttk.Button(dialog, text="SEARCH", command=search, style='CIA.TButton').pack(pady=5)

    def show_all_dialog(self):
        """Диалог показа всех персонажей"""
        dialog = tk.Toplevel(self.root)
        dialog.title("ALL CHARACTERS")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.geometry("600x400")

        text_area = scrolledtext.ScrolledText(dialog,
                                              font=('Courier', 9),
                                              bg=self.colors['bg_dark'],
                                              fg=self.colors['terminal_green'])
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text_area.insert(tk.END, "LOADING CHARACTER DATABASE...\n")

        def load_characters():
            characters = []
            next_url = self.base_url

            while next_url and len(characters) < 100:  # Ограничим 100 персонажами
                response = requests.get(next_url)
                if response.status_code == 200:
                    data = response.json()
                    characters.extend(data.get('results', []))
                    next_url = data.get('info', {}).get('next')

            text_area.delete(1.0, tk.END)
            for char in characters:
                status = "🟢" if char['status'] == 'Alive' else "🔴" if char['status'] == 'Dead' else "🟡"
                text_area.insert(tk.END,
                                 f"{char['id']:4d} {status} {char['name'][:30]:30} | {char['species']}\n")

        dialog.after(100, load_characters)

    def show_favorites(self):
        """Показать избранное"""
        if not self.favorites:
            messagebox.showinfo("FAVORITES", "NO FAVORITES SAVED")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("FAVORITE CHARACTERS")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.geometry("500x300")

        text_area = scrolledtext.ScrolledText(dialog,
                                              font=('Courier', 10),
                                              bg=self.colors['bg_dark'],
                                              fg=self.colors['terminal_yellow'])
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text_area.insert(tk.END, "⭐ FAVORITE CHARACTERS ⭐\n\n")

        for char_id in self.favorites:
            response = requests.get(f"{self.base_url}/{char_id}")
            if response.status_code == 200:
                char = response.json()
                text_area.insert(tk.END, f"ID {char_id}: {char['name']}\n")

    def load_random_character(self):
        """Загрузка случайного персонажа"""
        char_id = random.randint(1, self.total_characters)
        self.get_character_info(char_id)

    def toggle_favorite(self):
        """Добавить/удалить из избранного"""
        if self.current_character:
            char_id = self.current_character.get('id')
            if char_id in self.favorites:
                self.favorites.remove(char_id)
                self.log(f"REMOVED FROM FAVORITES: {self.current_character.get('name')}")
                self.fav_btn.config(text="⭐ ADD TO FAVORITES")
            else:
                self.favorites.add(char_id)
                self.log(f"ADDED TO FAVORITES: {self.current_character.get('name')}")
                self.fav_btn.config(text="★ REMOVE FROM FAVORITES")

    def copy_character_data(self):
        """Копирование данных персонажа"""
        if self.current_character:
            self.root.clipboard_clear()
            self.root.clipboard_append(json.dumps(self.current_character, indent=2))
            self.log("CHARACTER DATA COPIED TO CLIPBOARD")

    def find_similar(self):
        """Поиск похожих персонажей"""
        if not self.current_character:
            return

        species = self.current_character.get('species')
        response = requests.get(f"{self.base_url}", params={'species': species})

        if response.status_code == 200:
            data = response.json()
            characters = [c for c in data.get('results', [])
                          if c['id'] != self.current_character.get('id')]

            if characters:
                # Выбираем случайного похожего персонажа
                similar_char = random.choice(characters[:10])  # Берем из первых 10
                self.get_character_info(similar_char['id'])
                self.log(f"FOUND SIMILAR: {similar_char['name']}")
            else:
                self.log("NO SIMILAR CHARACTERS FOUND")

    def show_stats(self):
        """Показать статистику"""
        stats = f"""
╔{'═' * 40}╗
║{' ' * 15}DATABASE STATS{' ' * 15}║
╠{'═' * 40}╣
║ TOTAL CHARACTERS:    {self.total_characters:6d} ║
║ IN FAVORITES:        {len(self.favorites):6d} ║
║ HISTORY ENTRIES:     {len(self.history):6d} ║
║ CURRENT CHARACTER:   {self.current_character.get('id') if self.current_character else 'NONE':6} ║
╚{'═' * 40}╝
"""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, stats)
        self.photo_label.config(text="STATISTICS", image="")


def main():
    root = tk.Tk()
    app = CIAStyleRickMortyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

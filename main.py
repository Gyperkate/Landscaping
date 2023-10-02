import tkinter as tk
from tkinter import ttk
import sqlite3


# Класс Main  - это главное окно приложения
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

# Главное окно # Метод инициализации основного окна
    def init_main(self):
        toolbar = tk.Frame(bg='beige', bd=2)    # Создание панели инструментов
        toolbar.pack(side=tk.TOP, fill=tk.X)
        # Создание кнопок на панели инструментов
        # Кнопка "Добавить товар"
        self.add_img = tk.PhotoImage(file='add.png')
        btn_open_dialog = tk.Button(toolbar, text='Добавить товар ', command=self.open_dialog, bg='beige',
                                    bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)
        # Кнопка "Редактировать товар"
        self.update_img = tk.PhotoImage(file='edit.png')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='beige', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)
        # Кнопка "Удалить товар"
        self.delete_img = tk.PhotoImage(file='delete.png')
        btn_delete_dialog = tk.Button(toolbar, text='Удалить', bg='beige', bd=0, image=self.delete_img,
                                      compound=tk.TOP, command=self.delete_records)
        btn_delete_dialog.pack(side=tk.LEFT)
        # Кнопка "Поиск"
        self.search_img = tk.PhotoImage(file='search.png')
        btn_search = tk.Button(toolbar, text='Поиск', bg='beige', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)

        btn_search.pack(side=tk.LEFT)

        # Кнопка "Обновить"
        self.refresh_img = tk.PhotoImage(file='refresh.png')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='beige', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)
        # Создание таблицы для отображения данных
        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'category', 'price'), height=15, show='headings')
        # Установка параметров столбцов
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('description', width=365, anchor=tk.CENTER)
        self.tree.column('category', width=150, anchor=tk.CENTER)
        self.tree.column('price', width=100, anchor=tk.CENTER)
        # Установка заголовков столбцов
        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Наименование')
        self.tree.heading('category', text='Категория')
        self.tree.heading('price', text='Цена')

        self.tree.pack(side=tk.LEFT)
        # Добавление вертикальной полосы прокрутки
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

# Добавление данных
    def records(self, description, category, price):
        self.db.insert_data(description, category, price)
        self.view_records()

# Обновление данных
    def update_record(self, description, category, price):
        self.db.c.execute('''UPDATE accounting  SET description=?, category=?, price=? WHERE ID=?''',
                          (description, category, price, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

# Вывод данных
    def view_records(self):
        self.db.c.execute('''SELECT * FROM accounting''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

# Удаление данных
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM accounting WHERE id=? ''', (self.tree.set(selection_item, '#1'),))
            self.db.conn.commit()
            self.view_records()

# Поиск данных
    def search_records(self, description):
        description = ('%' + description + '%',)
        self.db.c.execute('''SELECT * FROM accounting WHERE description LIKE ?''', description)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

# Открытие дочернего окна
    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


# Дочернее окно
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить товар')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Наименование')
        label_description.place(x=50, y=50)

        label_select = tk.Label(self, text='Категория')
        label_select.place(x=50, y=80)

        label_price = tk.Label(self, text='Цена: ')
        label_price.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Смартфоны', u'Планшеты', 'Ноутбуки'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=150)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=150)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_money.get()))

        self.grab_set()
        self.focus_set()


# Класс обновления унаследованный от дочернего окна
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()


    def init_edit(self):
        self.title('Редактировать товары')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=150)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_description.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_money.get()))
        self.btn_ok.destroy()


    def default_data(self):
        self.db.c.execute('''SELECT * FROM accounting WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_description.insert(0, row[1])
        if row[2] != 'Смартфоны':
            self.combobox.current(1)
        self.entry_money.insert(0, row[3])


# Поиск по наименованию
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


# Создание базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('accounting.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS accounting (id integer primary key,description text, 
            category text, price real)''')
        self.conn.commit()

    def insert_data(self, description, category, price):
        self.c.execute('''INSERT INTO accounting (description, category, price) VALUES (?, ?, ?) ''',
                       (description, category, price))
        self.conn.commit()


# Основной код для запуска
if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Accounting")
    root.geometry("665x450+300+200")
    root.resizable(False, False)
    root.mainloop()

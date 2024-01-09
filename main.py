import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sqlite3


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Информация о кофе")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.create_database()
        self.create_table()
        self.create_table_view()

        # Вставка образцовых данных в таблицу кофе
        self.insert_sample_data()

        # Загрузка данных из базы данных SQLite
        data = self.fetch_data_from_database()
        self.populate_table_view(data)

    def create_database(self):
        # Подключение или создание базы данных SQLite в памяти
        self.connection = sqlite3.connect(':memory:')

    def create_table(self):
        # Создание таблицы кофе
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coffee (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                roast_degree TEXT,
                ground_or_whole TEXT,
                flavor_description TEXT,
                price REAL,
                packaging_volume INTEGER
            )
        ''')
        self.connection.commit()

    def create_table_view(self):
        layout = QVBoxLayout(self.central_widget)

        table_view = QTableView(self)
        layout.addWidget(table_view)

        # Настройка модели вручную с использованием QStandardItemModel
        self.model = QStandardItemModel(self)
        table_view.setModel(self.model)

        # Установка заголовков
        self.model.setHorizontalHeaderLabels(['ID', 'Название', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена', 'Объем упаковки'])

    def insert_sample_data(self):
        # Вставка образцовых данных в таблицу кофе
        cursor = self.connection.cursor()
        cursor.executemany('''
            INSERT INTO coffee (name, roast_degree, ground_or_whole, flavor_description, price, packaging_volume)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', [
            ('Эспрессо', 'Темный', 'Молотый', 'Интенсивный вкус', 2.5, 250),
            ('Латте', 'Средний', 'Молотый', 'Нежный и кремовый', 3.0, 300),
            ('Американо', 'Светлый', 'В зернах', 'Мягкий и разбавленный', 2.0, 200)
        ])
        self.connection.commit()

    def fetch_data_from_database(self):
        # Извлечение данных из таблицы кофе
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM coffee")
        data = cursor.fetchall()

        return data

    def populate_table_view(self, data):
        for row_index, row_data in enumerate(data):
            for col_index, col_value in enumerate(row_data):
                item = QStandardItem(str(col_value))
                self.model.setItem(row_index, col_index, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())

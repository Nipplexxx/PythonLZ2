from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
import psycopg2
import json

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}

def create_database():
    """Создает базу данных и таблицы, если они отсутствуют."""
    try:
        with psycopg2.connect(**DB_CONFIG) as connection:
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    login VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(50) NOT NULL,
                    fio VARCHAR(100),
                    email VARCHAR(100),
                    phone VARCHAR(20)
                );

                CREATE TABLE IF NOT EXISTS logs (
                    id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(id),
                    action VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS json_table (
                    id SERIAL PRIMARY KEY,
                    data JSON
                );
                """)
    except Exception as e:
        print("Ошибка при создании базы данных:", e)

class MainScreen(Screen):
    pass

class QueryScreen(Screen):
    query_input = ObjectProperty(None)
    query_output = ObjectProperty(None)

    def execute_query(self):
        """Выполняет пользовательский SQL-запрос."""
        try:
            with psycopg2.connect(**DB_CONFIG) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(self.query_input.text)
                    if cursor.description:
                        rows = cursor.fetchall()
                        self.query_output.text = "\n".join(map(str, rows))
                    else:
                        self.query_output.text = "Запрос выполнен успешно."
        except Exception as e:
            self.query_output.text = f"Ошибка: {e}"

class TableScreen(Screen):
    table_name_input = ObjectProperty(None)
    table_output = ObjectProperty(None)

    def show_table(self):
        """Выводит данные из указанной таблицы."""
        try:
            with psycopg2.connect(**DB_CONFIG) as connection:
                with connection.cursor() as cursor:
                    table_name = self.table_name_input.text
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    self.table_output.text = "\n".join(map(str, rows))
        except Exception as e:
            self.table_output.text = f"Ошибка: {e}"

class JSONScreen(Screen):
    json_input = ObjectProperty(None)
    message_label = ObjectProperty(None)

    def save_json(self):
        """Сохраняет данные в формате JSON в базу данных."""
        try:
            json_data = json.loads(self.json_input.text)
            with psycopg2.connect(**DB_CONFIG) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO json_table (data) VALUES (%s)", (json.dumps(json_data),))
                    self.message_label.text = "Данные успешно сохранены."
        except Exception as e:
            self.message_label.text = f"Ошибка: {e}"

class CustomScreenManager(ScreenManager):
    pass

class Lab4App(App):
    def build(self):
        create_database()

        manager = CustomScreenManager(transition=FadeTransition())

        manager.add_widget(MainScreen(name="main"))
        manager.add_widget(QueryScreen(name="query"))
        manager.add_widget(TableScreen(name="table"))
        manager.add_widget(JSONScreen(name="json"))

        return manager

kv_content = """
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Button:
            text: "Выполнить запрос"
            on_press: root.manager.current = "query"

        Button:
            text: "Просмотр таблицы"
            on_press: root.manager.current = "table"

        Button:
            text: "Добавить JSON"
            on_press: root.manager.current = "json"

<QueryScreen>:
    query_input: query_input
    query_output: query_output

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        TextInput:
            id: query_input
            hint_text: "Введите SQL-запрос"
            multiline: True

        Button:
            text: "Выполнить"
            on_press: root.execute_query()

        Label:
            id: query_output
            text: "Результат выполнения запроса"

        Button:
            text: "Назад"
            on_press: root.manager.current = "main"

<TableScreen>:
    table_name_input: table_name_input
    table_output: table_output

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        TextInput:
            id: table_name_input
            hint_text: "Введите имя таблицы"

        Button:
            text: "Показать таблицу"
            on_press: root.show_table()

        Label:
            id: table_output
            text: "Данные таблицы"

        Button:
            text: "Назад"
            on_press: root.manager.current = "main"

<JSONScreen>:
    json_input: json_input
    message_label: message_label

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        TextInput:
            id: json_input
            hint_text: "Введите JSON данные"
            multiline: True

        Button:
            text: "Сохранить JSON"
            on_press: root.save_json()

        Label:
            id: message_label
            text: ""

        Button:
            text: "Назад"
            on_press: root.manager.current = "main"
"""

from kivy.lang import Builder
Builder.load_string(kv_content)

if __name__ == "__main__":
    Lab4App().run()

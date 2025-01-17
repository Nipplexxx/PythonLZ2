from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from random import choice
import webbrowser

# Список шрифтов для случайного выбора
FONTS = ['Roboto', 'DejaVuSans', 'Arial']

class LabWorkApp(App):
    text_length = StringProperty("Длина текста: 0")

    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # **1. Таблица для ввода данных из кнопок**
        button_table = GridLayout(cols=3, size_hint=(1, 0.2))
        for i in range(9):
            btn = Button(text=f"Кнопка {i + 1}")
            btn.bind(on_press=lambda instance: self.add_button_text(instance))
            button_table.add_widget(btn)
        self.button_output = Label(text="Вывод текста кнопки")
        root.add_widget(button_table)
        root.add_widget(self.button_output)

        # **2. Панель с ссылками (уже выполнено)**
        link_panel = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)
        self.link_display = TextInput(text="Выберите ссылку", readonly=True, size_hint=(0.4, 1))
        link_panel.add_widget(self.link_display)

        links = [
            ("Kivy Docs", "https://kivy.org/doc/stable"),
            ("Python", "https://www.python.org"),
            ("GitHub", "https://github.com"),
            ("Google", "https://www.google.com"),
        ]

        for name, url in links:
            button = Button(text=name, size_hint=(0.15, 1))
            button.bind(on_press=lambda instance, u=url: self.open_link(u))
            link_panel.add_widget(button)

        root.add_widget(link_panel)

        # **3. FloatLayout и StackLayout**
        float_stack_layout = FloatLayout(size_hint=(1, 0.3))
        stack_layout = StackLayout(size_hint=(0.8, 0.8), pos_hint={'x': 0.1, 'y': 0.1})
        for i in range(5):
            stack_layout.add_widget(Button(text=f"Stack {i + 1}", size_hint=(0.3, 0.2)))
        float_stack_layout.add_widget(stack_layout)
        root.add_widget(float_stack_layout)

        # **4. AnchorLayout с сеткой**
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.2))
        grid_in_anchor = GridLayout(cols=3, rows=1, size_hint=(None, None), size=(300, 100))
        for i in range(3):
            grid_in_anchor.add_widget(Button(text=f"Сетка {i + 1}"))
        anchor_layout.add_widget(grid_in_anchor)
        root.add_widget(anchor_layout)

        # **5. Абсолютные координаты и размеры**
        absolute_layout = FloatLayout(size_hint=(1, 0.2))
        absolute_layout.add_widget(Button(text="Абсолют 1", size_hint=(None, None), size=(120, 50), pos=(50, 50)))
        absolute_layout.add_widget(Button(text="Абсолют 2", size_hint=(None, None), size=(100, 40), pos=(200, 30)))
        root.add_widget(absolute_layout)

        # **6. FloatLayout и GridLayout**
        float_grid_layout = FloatLayout(size_hint=(1, 0.3))
        grid_layout = GridLayout(cols=2, size_hint=(0.6, 0.6), pos_hint={'x': 0.2, 'y': 0.2})
        for i in range(5):
            grid_layout.add_widget(Button(text=f"Grid {i + 1}"))
        float_grid_layout.add_widget(grid_layout)
        root.add_widget(float_grid_layout)

        # **7. Таблица с добавлением данных и случайным шрифтом**
        data_table = GridLayout(cols=2, size_hint=(1, 0.3))
        self.input1 = TextInput(hint_text="Введите фамилию", multiline=False)
        self.input2 = TextInput(hint_text="Введите имя", multiline=False)
        self.input3 = TextInput(hint_text="Введите возраст", multiline=False)
        self.input4 = TextInput(hint_text="Введите email", multiline=False)

        data_table.add_widget(Label(text="Фамилия:"))
        data_table.add_widget(self.input1)
        data_table.add_widget(Label(text="Имя:"))
        data_table.add_widget(self.input2)
        data_table.add_widget(Label(text="Возраст:"))
        data_table.add_widget(self.input3)
        data_table.add_widget(Label(text="Email:"))
        data_table.add_widget(self.input4)

        submit_button = Button(text="Добавить данные")
        submit_button.bind(on_press=self.add_data_with_font)
        data_table.add_widget(submit_button)
        self.data_label = Label(text="Добавленные данные появятся здесь", size_hint=(1, 0.2))
        data_table.add_widget(self.data_label)

        root.add_widget(data_table)

        # **8. Поля для ввода с длиной текста**
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        text_input = TextInput(hint_text="Введите текст", multiline=False)
        text_input.bind(text=self.update_text_length)
        input_layout.add_widget(text_input)
        input_layout.add_widget(Label(text=self.text_length))
        root.add_widget(input_layout)

        # **10. Слайдер для изменения размера кнопки** (уже выполнено)
        slider_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        slider_label = Label(text="Измените размер кнопки:", size_hint=(0.3, 1))
        self.slider = Slider(min=50, max=200, value=100, size_hint=(0.7, 1))
        self.slider.bind(value=self.on_slider_value_change)
        slider_layout.add_widget(slider_label)
        slider_layout.add_widget(self.slider)
        root.add_widget(slider_layout)

        # **11. Три колонки с виджетами через BoxLayout** (уже выполнено)
        column_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        for i in range(3):
            box = BoxLayout(orientation='vertical')
            for j in range(3):
                box.add_widget(Button(text=f"Колонка {i + 1} Виджет {j + 1}"))
            column_layout.add_widget(box)
        root.add_widget(column_layout)

        # **13. Вывод состояния кнопки (уже выполнено)**
        state_button = Button(text="Состояние кнопки", size_hint=(1, 0.1))
        state_button.bind(
            on_press=lambda instance: print("Кнопка нажата"),
            on_release=lambda instance: print("Кнопка отпущена")
        )
        root.add_widget(state_button)

        return root

    def add_button_text(self, instance):
        self.button_output.text = f"Нажата: {instance.text}"

    def add_data_with_font(self, instance):
        font = choice(FONTS)
        self.data_label.text = (
            f"[font={font}]Фамилия: {self.input1.text}\n"
            f"Имя: {self.input2.text}\n"
            f"Возраст: {self.input3.text}\n"
            f"Email: {self.input4.text}[/font]"
        )
        self.input1.text = ""
        self.input2.text = ""
        self.input3.text = ""
        self.input4.text = ""

    def update_text_length(self, instance, value):
        self.text_length = f"Длина текста: {len(value)}"

    def open_link(self, url):
        self.link_display.text = url
        webbrowser.open(url)

    def on_slider_value_change(self, instance, value):
        self.data_label.font_size = value

if __name__ == "__main__":
    LabWorkApp().run()
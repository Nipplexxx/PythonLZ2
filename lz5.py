from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, WipeTransition, FadeTransition, SwapTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.animation import Animation, AnimationTransition
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty
import random

class RotatingWidget(RelativeLayout):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.3, 0.3, 0.7, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def start_rotation(self):
        anim = Animation(angle=360, duration=2, t=AnimationTransition.linear)
        anim &= Animation(size=(self.width * 1.5, self.height * 1.5), duration=1, t=AnimationTransition.in_out_sine)
        anim.start(self)

class ColoredBackground(Widget):
    def __init__(self, color, **kwargs):
        super().__init__(**kwargs)
        self.rgba = color
        with self.canvas.before:
            Color(*self.rgba)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

# Экран с приветствием
class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ColoredBackground((0.2, 0.6, 0.8, 1)))

        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        self.title = Label(text="Добро пожаловать!", font_size=24, size_hint_y=None, height=50)
        layout.add_widget(self.title)

        self.start_button = Button(text="Начать", size_hint=(None, None), size=(200, 50), pos_hint={"center_x": 0.5})
        self.start_button.bind(on_press=self.go_to_next)
        layout.add_widget(self.start_button)

        self.add_widget(layout)

    def go_to_next(self, instance):
        self.manager.transition = SlideTransition(direction="left", duration=1)
        self.manager.current = "gradient_screen"

# Экран с переливающимся фоном
class GradientScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = ColoredBackground((1, 0, 0, 1))
        self.add_widget(self.bg)
        self.start_gradient_animation()

        next_button = Button(text="Далее", size_hint=(None, None), size=(200, 50), pos_hint={"center_x": 0.5, "center_y": 0.1})
        next_button.bind(on_press=self.go_to_next)
        self.add_widget(next_button)

    def start_gradient_animation(self):
        anim = (Animation(rgba=(0, 1, 0, 1), duration=1) + Animation(rgba=(0, 0, 1, 1), duration=1))
        anim.repeat = True
        anim.start(self.bg)

    def go_to_next(self, instance):
        self.manager.transition = WipeTransition(duration=1)
        self.manager.current = "image_sequence"

# Экран с поочередно появляющимися изображениями
class ImageSequenceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.image1 = Label(text="Изображение 1", font_size=24)
        self.image2 = Label(text="Изображение 2", font_size=24)
        self.image3 = Label(text="Изображение 3", font_size=24)

        layout.add_widget(self.image1)
        layout.add_widget(self.image2)
        layout.add_widget(self.image3)

        next_button = Button(text="Далее", size_hint=(None, None), size=(200, 50), pos_hint={"center_x": 0.5})
        next_button.bind(on_press=self.go_to_next)
        layout.add_widget(next_button)

        self.add_widget(layout)
        self.start_sequence_animation()

    def start_sequence_animation(self):
        anim1 = Animation(opacity=0, duration=1) + Animation(opacity=1, duration=1)
        anim1.repeat = True
        anim1.start(self.image1)

        anim2 = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)
        anim2.repeat = True
        anim2.start(self.image2)

        anim3 = Animation(opacity=0, duration=1) + Animation(opacity=1, duration=1)
        anim3.repeat = True
        anim3.start(self.image3)

    def go_to_next(self, instance):
        self.manager.transition = FadeTransition(duration=1)
        self.manager.current = "interactive_screen"

# Экран с виджетами, реагирующими на нажатие
class InteractiveScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = RelativeLayout()
        self.button = Button(text="Переместить", size_hint=(None, None), size=(150, 50), pos=(100, 100))
        layout.add_widget(self.button)

        self.button.bind(on_press=self.animate_button)

        next_button = Button(text="Крестики-нолики", size_hint=(None, None), size=(200, 50), pos_hint={"center_x": 0.5, "center_y": 0.1})
        next_button.bind(on_press=self.go_to_next)
        layout.add_widget(next_button)

        self.add_widget(layout)

    def animate_button(self, instance):
        new_x = random.randint(50, 300)
        new_y = random.randint(50, 500)
        anim = Animation(pos=(new_x, new_y), duration=0.5)
        anim.start(instance)

    def go_to_next(self, instance):
        self.manager.transition = SwapTransition(duration=1)
        self.manager.current = "tic_tac_toe"

# Основная игра "Крестики-нолики"
class TicTacToeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ColoredBackground((0.4, 0.4, 0.8, 1)))

        self.players = ("", "")
        self.turn = "X"
        self.board = [None] * 9

        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        self.status_label = Label(text="Ход: X", font_size=24, color=(1, 1, 1, 1), size_hint_y=None, height=50)
        self.layout.add_widget(self.status_label)

        self.grid = GridLayout(cols=3, spacing=5, size_hint_y=0.6)
        for i in range(9):
            btn = Button(font_size=32, text="", background_color=(0.3, 0.3, 0.7, 1))
            btn.bind(on_press=self.make_move)
            self.grid.add_widget(btn)
            self.board[i] = btn
        self.layout.add_widget(self.grid)

        restart_button = Button(text="Играть снова", font_size=24, size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5})
        restart_button.bind(on_press=self.restart_game)
        self.layout.add_widget(restart_button)

        self.add_widget(self.layout)

    def make_move(self, instance):
        if instance.text == "":
            instance.text = self.turn
            if self.check_winner():
                self.status_label.text = f"Победитель: {self.turn}"
                self.disable_board()
                return
            self.turn = "O" if self.turn == "X" else "X"
            self.status_label.text = f"Ход: {self.turn}"

    def check_winner(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for condition in win_conditions:
            if (self.board[condition[0]].text == self.board[condition[1]].text ==
                    self.board[condition[2]].text != ""):
                return True
        return False

    def disable_board(self):
        for btn in self.board:
            btn.disabled = True

    def restart_game(self, instance):
        self.turn = "X"
        for btn in self.board:
            btn.text = ""
            btn.disabled = False
        self.status_label.text = f"Ход: {self.turn}"

# Менеджер экранов
class EnhancedScreenManager(ScreenManager):
    pass

class Lab5App(App):
    def build(self):
        sm = EnhancedScreenManager()
        sm.add_widget(FirstScreen(name="screen1"))
        sm.add_widget(GradientScreen(name="gradient_screen"))
        sm.add_widget(ImageSequenceScreen(name="image_sequence"))
        sm.add_widget(InteractiveScreen(name="interactive_screen"))
        sm.add_widget(TicTacToeScreen(name="tic_tac_toe"))
        return sm

if __name__ == "__main__":
    Lab5App().run()

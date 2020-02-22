from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput

from kivy.graphics import (Color, Rectangle, Line)

from kivy.config import Config

Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", "1000")
Config.set("graphics", "height", "650")


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)

        with self.canvas:
            color


class LightBotApp(App):
    def build(self):
        main_layout = BoxLayout()
        control_layout = BoxLayout(orientation = "vertical")

        code = CodeInput()
        start = Button(text="Interpret", size_hint_y=None, height=100)

        control_layout.add_widget(code)
        control_layout.add_widget(start)
        main_layout.add_widget(control_layout)
        main_layout.add_widget(GameWidget())
        return main_layout


if __name__ == "__main__":
    LightBotApp().run()

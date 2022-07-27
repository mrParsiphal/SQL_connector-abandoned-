from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)


from kivy.core.window import Window
Window.clearcolor = (.24, .55, .55, 0.2)


class window(BoxLayout):
    t = ObjectProperty(None)

    def on_touch_move(self, touch):
        if (touch.x < self.t.width / 2 + self.t.center_x) and (touch.x > self.t.center_x - self.t.width / 2) and \
                (touch.y < self.t.height / 2 + self.t.center_y) and (touch.y > self.t.center_y - self.t.height / 2):
            self.t.center_x = touch.x
            self.t.center_y = touch.y


class MainApp(App):
    def build(self):
        return window()


if __name__ == '__main__':
    MainApp().run()
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_string('''
<Root>:
    Camera:
        id: camera
        resolution: (640, 480)
        play: True
''')

class Root(BoxLayout):
    def root(self):
        return

class Camera(App):
    def build(self):
        return Root()

Camera().run()

import kivy,math
kivy.require('1.10.0')
from kivy.properties import NumericProperty,StringProperty,ListProperty,BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color,Line
from kivy.lang import Builder
from kivy.uix.image import Image


Builder.load_string('''
<LandingForm>:
    Label:
        text: "ela"
    TextInput:
        id: iAmTxt
        text: 'txt'
    Button:
        text: 'print LandingFormInput [0, 1, 2]'
        on_release: print("segamao")
''')

class LandingForm(Widget):
    def __init__(self, **kwargs):
        super(LandingForm, self).__init__(**kwargs)
        self.bind(pos=self.change)
    def change(self,*args):
        self.center = self.center

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty,StringProperty, ListProperty,BoundedNumericProperty
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from sectorLabel import SectorLabel
from customcolor import CustomColor
from kivy.uix.textinput import TextInput


class InputLabel(Widget):
    labeltxt = StringProperty()
    inputtext = StringProperty()
    def __init__(self, **kwargs):
        super(InputLabel,self).__init__ (**kwargs)

        self.add_widget(Label(text = str(self.labeltxt),font_size = '16sp'))
        self.add_widget(TextInput(text=str(self.inputtext),font_size = '16sp'))

        self.bind(pos = self._update)
        self.bind(size = self._update)
        self.bind(on_text_validate = self._upgrade)

    def _update(self,*args):
        self.children[0].pos = [self.x,self.y]
        self.children[1].pos = [self.x+self.size[0],self.y+self.size[1]]
        self.size = (self.size[0],self.size[1])

    def _upgrade(self,*args):
        global inputtext
        inputtext = self.children[1].text

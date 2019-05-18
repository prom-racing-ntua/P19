import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import AliasProperty,NumericProperty,StringProperty, ListProperty,BoundedNumericProperty
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from sectorLabel import SectorLabel
from kivy.uix.progressbar import ProgressBar
from progress import MDProgressBar

Builder.load_string('''
<BrakeGauge>:
    MDProgressBar:
        id: brakepb
        max: 1000
        value: 18
        orientation:'vertical'
        color1:[0.37,0.35,0.35,1]
        color2:[1,0,0,1]
        pos: self.x,self.y
        size: self.size[0],self.size[1]
''')




class BrakeGauge (Widget):

    brakevalue = NumericProperty()
    def __init__(self,**kwargs):
        super(BrakeGauge,self).__init__(**kwargs)
        print ('mphka __init__ brakegauge')
        self.brakelabel=Label(text = 'BRAKE',font_size='10sp')
        self.add_widget(self.brakelabel)
        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(brakevalue = self._upgrade)

    def _update(self,*args):
        self.ids.brakepb.center = self.center_x,self.center_y
        self.ids.brakepb.size = self.size[0],self.size[1]
        self.brakelabel.pos = self.center_x-10,self.y-self.brakelabel.size[1]
        self.brakelabel.size = 50,20

    def _upgrade(self, *args):
        self.ids.brakepb.value = self.brakevalue

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

Builder.load_string('''
<BrakeGauge>:
    ProgressBar:
        id: brakepb
        max: 1000
        value: self.brakevalue
        pos: self.x,self.y
        size: self.size[0],self.size[1]
''')




class BrakeGauge (Widget):
    
    brakevalue = NumericProperty()
    def __init__(self,**kwargs):
        super(BrakeGauge,self).__init__(**kwargs)
        print ('mphka __init__ brakegauge')

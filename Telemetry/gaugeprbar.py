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
<TPSGauge>:
    MDProgressBar:
        id: tpspb
        max: 1000
        value: 500
        pos: self.x,self.y
        orientation:'vertical'
        color1: [0.37,0.35,0.35,1]
        color2: [0,1,0,1]
        size: self.size[0],self.size[1]
''')


class TPSGauge (Widget):

    tpsvalue = NumericProperty()
    def __init__(self,**kwargs):
        super(TPSGauge,self).__init__(**kwargs)
        print ('mphka __init__ TPSgauge')
        self.bind(pos = self._update)
        self.bind(size = self._update)
        self.bind(tpsvalue = self._upgrade)
        self.tpslabel = Label(text='TPS',font_size='10sp')
        self.add_widget(self.tpslabel)
        # self.bind(value = self._upgrade)

    def _update(self, *args):
        self.ids.tpspb.center = self.center_x, self.center_y
        self.ids.tpspb.size = self.size[0],self.size[1]
        self.tpslabel.pos = self.center_x-5,self.y-self.tpslabel.size[1]
        self.tpslabel.size = 40,20

    def _upgrade(self,*args):
        self.ids.tpspb.value = self.tpsvalue

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty,StringProperty, ListProperty,BoundedNumericProperty
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from sectorLabel import SectorLabel
from kivy.uix.progressbar import ProgressBar

class TPSGauge(Widget) :
    tpsvalue = NumericProperty()

    def __init__(self, **kwargs):
        super(TPSGauge,self).__init__ (**kwargs)
        print ("mphka __init__ tpsgauge")
        self.tpspb = ProgressBar(max=1000,value = self.tpsvalue)
        # self.brakepb = ProgressBar(max = 1000)

        self.add_widget(self.tpspb)
        # self.add_widget(self.brakepb)

        self.bind(pos = self._update)
        self.bind(size = self._update)
        self.bind(value = self._vupdate)

    def _update(self,*args):
        self.center = self.center_x, self.center_y
        self.size = self.size[0],self.size[1]

    def _vupdate(self,*args):
        self.tpspb.value = self.tpsvalue

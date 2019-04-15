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


class SpeedLabel(Widget):

    ## the values of the labels
    currentspeed = NumericProperty()
    customcolor = ListProperty([])

    def __init__(self, **kwargs):
        super(SpeedLabel, self).__init__(**kwargs)
        ## Create the labels
        self.speedlabel = SectorLabel(text = str(self.currentspeed) ,lineclr=[1,1,1,0], color = [0,0,1,1] , font_size = '60sp')
        self.signlabel = SectorLabel (text = "km/h" , color = [1,1,1,1] , font_size = '15sp' )
        self.add_widget(self.speedlabel)
        self.add_widget(self.signlabel)

        ##create the bindings to update size,pos and values
        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(currentspeed=self._changespeed)

    def _update (self, *args):
        ##fixing the positions and size
        self.speedlabel.center = (self.center_x , self.y)
        self.speedlabel.size = self.size[0],self.size[1]
        # self.signlabel.size = self.size[0]/8,self.size[1]/8
        self.signlabel.center = (self.center_x,self.center_y-self.size[1])

    #def _changetime (self, *args):

    def _changespeed (self, *args):
        # self.gearlabel.color = [1,0,0,1]
        self.speedlabel.text = str(int(self.currentspeed))
        # self.gearlabel.color = self.customcolor

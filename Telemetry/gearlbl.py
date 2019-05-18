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


class GearLabel(Widget):

    ## the values of the labels
    currentgear = NumericProperty()
    customcolor = ListProperty([])

    def __init__(self, **kwargs):
        super(GearLabel, self).__init__(**kwargs)
        ## Create the labels
        self.gearlabel = SectorLabel(text = str(self.currentgear) ,lineclr=[1,1,1,0], color = [1,1,0,1] , font_size = '70sp')
        # self.signlabel = SectorLabel(text = "gear" , color = [1,1,1,1] , font_size = '15sp')
        self.add_widget(self.gearlabel)
        # self.add_widget(self.signlabel)

        ##create the bindings to update size,pos and values
        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(currentgear=self._changegear)

    def _update (self, *args):
        ##fixing the positions and size
        self.gearlabel.center = (self.center_x , self.y)
        self.gearlabel.size = self.size[0],self.size[1]
        # self.signlabel.center = (self.center_x,self.center_y-self.size[1])

    #def _changetime (self, *args):

    def _changegear (self, *args):
        # self.gearlabel.color = [1,0,0,1]
        self.gearlabel.text = str(int(self.currentgear))
        # self.gearlabel.color = self.customcolor

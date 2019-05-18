import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty,StringProperty, ListProperty
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from sectorLabel import SectorLabel

##### IN PROGRESS ######

class SectorsV2(Widget):

    ## values of the indexing labels
    sectornames = ListProperty([])
    ## values
    sectorvalues = ListProperty([])
    ##
    customcolor = ListProperty([])

    def __init__(self, **kwargs):
        super(SectorsV2, self).__init__(**kwargs)
        # print (self.sectornames)
        ## create each sectorlabel index and value
        for i in self.sectornames :
            self.add_widget(SectorLabel(text = str(self.sectornames), bgclr =[1,1,1,0] , font_size = '18sp'))
        # self.bind(pos = self._update)
        # self.bind(size = self._update)
        # pos=[self.x,self.y+self.offset],

    def _update(self, *args):
        # self.pos = self.x , self.y
        self.size = self.size[0],self.size[1]

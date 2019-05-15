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

class TempSectors(Widget):

    ## values of the indexing labels
    sectorname = StringProperty()
    ## the values
    sectorvalue = StringProperty()
    ##
    customcolor = ListProperty([])
    offset = NumericProperty(0)

    def __init__(self, **kwargs):
        super(TempSectors, self).__init__(**kwargs)
        # print (self.sectornames[1])
        # print ('x,y,size0,size1')
        # print (self.x,self.y,self.size[0],self.size[1])
        self.sectorindex = SectorLabel(text = self.sectorname ,bgclr = [1,1,1,0],lineclr = [1,1,1,1],color = [0.1,1,0.9,1],font_size='16sp')
        self.valuelabel = SectorLabel(text = self.sectorvalue , bgclr = [1,1,1,0],lineclr=[1,1,1,1],color = [0.1,1,0.20], font_size = '16sp')
        self.add_widget (self.sectorindex)
        self.add_widget(self.valuelabel)
        self.bind(size =self._update)
        self.bind(pos = self._update)

    def _update(self,*args):
        self.sectorindex.size = self.size[0],self.size[1]
        self.sectorindex.pos = self.x,self.y
        # self.sectorindex.text.center = self.center_x,self.center_y

        self.valuelabel.size = self.size[0],self.size[1]
        self.valuelabel.pos = self.x+self.sectorindex.size[0],self.y
        # self.valuelabel.text.center = self.center_x,self.center_y

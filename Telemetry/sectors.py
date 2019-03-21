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

Builder.load_string('''
<Sectors>:
    canvas:
        Color:
            rgba: self.customcolor
        Line:
            rectangle: self.x,self.y,self.width,self.height
            width: 1
''')



class Sectors(Widget):

    ## the values of the labels
    sectorname = StringProperty("")
    time = StringProperty("") ## serial input
    best = StringProperty("00:00")
    previousbest = StringProperty("")
    currenttime = StringProperty("")
    customcolor = ListProperty([])

    def __init__(self, **kwargs):
        super(Sectors, self).__init__(**kwargs)
        ## Create the labels
        self.sectorlabel = SectorLabel(text = " " ,bgclr=[1,1,1,1], color = [0,1,1,1] , font_size = '22sp')
        self.bestlabel = SectorLabel(text = "00:00" ,bgclr=[1,1,1,1], color = [0,1,0,1] , font_size = '22sp')
        self.previouslabel = SectorLabel(text = "00:00" ,bgclr=[1,1,1,1], color = [1,0,0,1] , font_size = '22sp')
        self.currentlabel = SectorLabel(text = "00:00" ,bgclr=[1,1,1,1], color = [0,0,1,1] , font_size = '22sp')
        self.add_widget(self.sectorlabel)
        self.add_widget(self.currentlabel)
        self.add_widget(self.previouslabel)
        self.add_widget(self.bestlabel)


        ##create the bindings to update size,pos and values
        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(currenttime=self._changetime)
        self.bind(best=self._changebest)

    def _update (self, *args):
        ##fixing the positions and size
        h = self.height/4
        self.sectorlabel.center = (self.center_x , self.y+4*h)
        self.currentlabel.center = (self.center_x , self.y + 3*h)
        self.previouslabel.center = (self.center_x , self.center_y)
        self.bestlabel.center = (self.center_x , self.y+h)
        self.sectorlabel.size[1] = self.size[1]/4
        self.currentlabel.size[1] = self.size[1]/4
        self.previouslabel.size[1] = self.size[1]/4
        self.bestlabel.size[1] = self.size[1]/4

    def _changetime (self, *args):
        self.currentlabel.text = self.currenttime
        self.previouslabel.text = self.previousbest
        self.bestlabel.text = self.best

    def _changebest (self, *args):
        if self.currenttime < self.best :
            self.previousbest = self.best
            self.best = self.currenttime

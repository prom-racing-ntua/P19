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


# Builder.load_string('''
# <Sectors>:
#     canvas:
#         Color:
#             rgba: self.customcolor
#
# ''')



class Sectors(Widget):

    ## the values of the labels
    sectorname = StringProperty(" ")
    time = StringProperty("") ## serial input
    best = StringProperty("1000")
    previousbest = StringProperty("")
    currenttime = StringProperty("")
    customcolor = ListProperty([])

    def __init__(self, **kwargs):
        super(Sectors, self).__init__(**kwargs)
        ## Create the labels
        self.sectorlabel = SectorLabel(text = self.sectorname ,lineclr=[1,1,1,1], color = [0,1,1,1] , font_size = '18sp')
        self.bestlabel = SectorLabel(text = self.best ,lineclr=[1,1,1,1], color = [0,1,0,1] , font_size = '18sp')
        self.previouslabel = SectorLabel(text = self.previousbest ,lineclr=[1,1,1,1], color = [1,0,0,1] , font_size = '18sp')
        self.currentlabel = SectorLabel(text = self.currenttime ,lineclr=[1,1,1,1], color = [0,0,1,1] , font_size = '18sp')
        self.add_widget(self.sectorlabel)
        self.add_widget(self.currentlabel)
        self.add_widget(self.previouslabel)
        self.add_widget(self.bestlabel)


        ##create the bindings to update size,pos and values
        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(currenttime=self._changebest)
        #self.bind(best=self._changebest)

    def _update (self, *args):
        ##fixing the positions and size
        h = self.height/4
        self.sectorlabel.center = (self.center_x , self.y+3*h)
        self.currentlabel.center = (self.center_x , self.y + 2*h)
        self.previouslabel.center = (self.center_x , self.y+h)
        self.bestlabel.center = (self.center_x , self.y)
        self.sectorlabel.size = self.size[0],self.size[1]/4
        self.currentlabel.size = self.size[0],self.size[1]/4
        self.previouslabel.size = self.size[0],self.size[1]/4
        self.bestlabel.size = self.size[0],self.size[1]/4

    #def _changetime (self, *args):


    def _changebest (self, *args):
        if float(self.currenttime) < float(self.best) :
            self.previousbest = self.best
            self.best = self.currenttime
        self.currentlabel.text =self.currenttime[0:5]
        self.previouslabel.text = self.previousbest[0:5]
        self.bestlabel.text = self.best[0:5]

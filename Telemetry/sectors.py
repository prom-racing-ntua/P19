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

Builder.load_string('''
<Sectors>:
    canvas:
        color:
            rgba : self.customcolor
        Rectangle:
            pos: self.center_x-self.size[0]/2, self.center_y-self.size[1]/2
            size: self.size[0]*0.98,self.size[1]
''')



class Sectors(Widget):

    ## the values of the labels
    sectorname = StringProperty("")
    time = StringProperty("") ## serial input
    best = StringProperty("00:00")
    previousbest = StringProperty("")
    currenttime = StringProperty("")
    customcolor = ListProperty()


def __init__(self, **kwargs):
    super(Sectors, self).__init__(**kwargs)
    ## Create the labels
    self.sectorlabel = Label (text = "" , color = (0,1,1,1) , font_size = '10sp')
    self.bestlabel = Label(text = "00:00" , color = (0,1,0,1) , font_size = '10sp')
    self.previouslabel = Label(text = "00:00" , color = (1,0,0,1) , font_size = '10sp')
    self.currentlabel = Label (text = "00:00" , color = (0,0,1,1) , font_size = '10sp')
    self.add_widget(sectorlabel)
    self.add_widget(currentlabel)
    self.add_widget(previouslabel)
    self.add_widget(bestlabel)


    ##create the bindings to update size,pos and values
    self.bind = (self.pos , _update)
    self.bind = (self.size , _update)
    self.bind = (self.currenttime , _changetime)
    self.bind = (self.best , _changebest)

def _update (self, *args):
    ##fixing the positions and size
    h = self.height/4
    self.sectorlabel.center = (self.center_x , self.center_y + 2*h)
    self.currentlabel.center = (self.center_x , self.center_y + h)
    self.previouslabel.center = (self.center_x , self.center_y - h)
    self.bestlabel.center = (self.center_x , self.center_y - 2*h)

def _changetime (self, *args):
    self.currentlabel.text = self.currenttime
    self.previouslabel.text = self.previoustime
    self.bestlabel.text = self.best

def _changebest (self, *args):
    if self.currenttime < self.best :
        self.previousbest = self.best
        self.best = self.currenttime

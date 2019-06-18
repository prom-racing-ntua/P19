import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty,StringProperty, ListProperty,BoundedNumericProperty
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from sectorLabel import SectorLabel
from customcolor import CustomColor
from inputwithlabel import InputLabel


class PopupWidget(BoxLayout):
    inputdefaults = ListProperty([])
    labeldefaults = ListProperty([])
    def __init__(self, **kwargs):
        super(PopupWidget,self).__init__ (**kwargs)

        self.cols=2
        self.rows=2
        self.spacing = 3
        # print ("mphka super __init__ tire")
        self.fl = BoxLayout(orientation = 'vertical')
        self.fr = BoxLayout(orientation = 'vertical')
        self.rl = BoxLayout(orientation = 'vertical')
        self.rr = BoxLayout(orientation = 'vertical')

        self.add_widget(self.fl)
        self.add_widget(self.fr)
        self.add_widget(self.rl)
        self.add_widget(self.rr)

        # for i,x in enumerate(self.children):
        #     print (i)
        #add labels
        for x in self.children:
            for y in range(5):
                x.add_widget(InputLabel(labeltxt = str(self.labeldefaults),inputtext = str(self.inputdefaults)))

        self.bind(pos = self._update)
        self.bind(size = self._update)
        # self.bind(on = self._upgrade)

    def _update(self,*args):
        self.pos= [self.x,self.y]
        self.size = (self.size[0],self.size[1])
        # print('eimai update')
        # print(self.x,self.y)
        # print (self.size)

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
<BrakeBiasPB>:
    MDProgressBar:
        id: brakebias
        max: 100
        value: 50
        pos: self.x,self.y
        orientation:'horizontal'
        color1: [0.37,0.35,0.35,1]
        color2: [0.57,0.55,0.55,1]
        size: self.size[0],self.size[1]
''')


class BrakeBiasPB (Widget):

    bbvalue = NumericProperty(60)
    def __init__(self,**kwargs):
        super(BrakeBiasPB,self).__init__(**kwargs)
        print ('mphka __init__ BBPB')
        self.backlabel = Label(text='REAR',font_size='10sp')
        self.add_widget(self.backlabel)
        self.frontlabel = Label(text='FRONT',font_size='10sp')
        self.add_widget(self.frontlabel)
        self.valuelabel = Label(text = str(self.ids.brakebias.value)+'%',font_size = '12.5sp')
        self.add_widget(self.valuelabel)
        self.bind(pos = self._update)
        self.bind(size = self._update)
        self.bind(bbvalue = self._upgrade)
        # print('################################ BRAKE BIAS')
        # print (self.ids)
        # self.bind(value = self._upgrade)

    def _update(self, *args):
        self.ids.brakebias.center = self.center_x, self.center_y
        self.ids.brakebias.size = self.size[0],self.size[1]
        self.backlabel.pos = self.x-self.backlabel.size[0],self.y-5
        self.backlabel.size = 50,20
        self.frontlabel.pos = self.x+self.size[0],self.y-6
        self.frontlabel.size =50,20
        self.valuelabel.pos = self.center_x-10,self.y+10
        self.valuelabel.size = 30,20
    def _upgrade(self,*args):
        self.ids.brakebias.value = self.bbvalue
        self.valuelabel.text = str(self.ids.brakebias.value)+'%'

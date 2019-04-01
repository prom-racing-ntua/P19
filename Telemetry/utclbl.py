import kivy
kivy.require('1.10.0')
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from kivy.uix.image import Image
from hover import HoverBehavior
from sectors import Sectors
from sectorLabel import SectorLabel
from datetime import *
from kivy.clock import Clock

from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty,ListProperty


class UtcLbl(SectorLabel):
    utcdate = StringProperty(datetime.utcnow().strftime('%Y-%m-%d'))
    utctime = StringProperty(datetime.utcnow().strftime('%H:%M:%S'))

    def __init__(self, **kwargs):
        super(UtcLbl, self).__init__(**kwargs)
        ## Create the labels
        self.datelabel = SectorLabel (text =str(self.utcdate)  , color = [1,0,0,1] , font_size = '20sp')
        self.timelabel = SectorLabel (text ="UTC"+str(self.utctime)  , color = [0,1,0,1] , font_size = '20sp')
        self.add_widget (self.datelabel)
        self.add_widget (self.timelabel)
        Clock.schedule_interval(self._updateutc,0.5)
        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(utctime = self._updateutc)


    def _updateutc(self, *args):
        # print ("yessssss")
        self.utcdate = datetime.utcnow().strftime('%d-%m-%Y')
        self.utctime = datetime.utcnow().strftime('%H:%M:%S')
        self.datelabel.text = str(self.utcdate)
        self.timelabel.text = "UTC "+str(self.utctime)

    def _update (self, *args):
        ##fixing the positions and size
        # print ("yesss pos")
        h = self.height/4
        self.datelabel.center = (self.center_x , self.center_y+h)
        self.timelabel.center = (self.center_x , self.center_y-h)
        self.datelabel.size = self.size[0],self.size[1]/2
        self.timelabel.size = self.size[0],self.size[1]/2

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

from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty,ListProperty

class WarningLabel(Widget):

    name = StringProperty()
    warncolor = ListProperty([1,1,1,1])
    max_value = 10
    min_value = 3
    sensorvalue = NumericProperty(1) #pare timi

    def __init__(self, **kwargs):

        super(WarningLabel, self).__init__(**kwargs)
        self.warninglabel = SectorLabel(text = str(self.name) ,lineclr=[1,1,1,0], color = self.warncolor, font_size = '20sp')
        self.add_widget(self.warninglabel)
        self.bind(pos=self._update)
        self.bind(size=self._update)

    def _update(self, *args):
        self.warninglabel.center = (self.center_x , self.y)
        self.warninglabel.size = self.size[0],self.size[1]

    def _changecolor(self, *args):
        if(sensorvalue >= max_value or sensorvalue <= min_value):
            self.warncolor = [1,0.09,0,1]

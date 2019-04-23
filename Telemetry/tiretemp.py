#tiretemp
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
# <TiretempLbl>:
#     canvas:
#         Color:
#             rgba: self.customcolor
#
# ''')

class TiretempLbl (Widget) :
    lblname = StringProperty ()
    tempclr = ListProperty ([])
    tiretemp = NumericProperty()
    mintemp = NumericProperty ()
    maxtemp = NumericProperty ()

    def __init__(self, **kwargs):
        super(TiretempLbl,self).__init__ (**kwargs)
        self.tirelabel = SectorLabel (text = str(tiretemp), lineclr = [1,1,1,1], bgclr = tempclr , font_size = '18sp')
        self.add_widget (self.tirelabel)
        ##create the bindings to update size,pos and values
        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(tiretemp=self._change)

    def _update(self,*args):
        self.tirelabel.center = (self.center_x,self.center_y)
        self.tirelabel.size = self.size[0],self.size[1]

    def _change (self,*args):
        self.tirelabel.bgclr = tempclr
        self.tirelabel.text = str(tiretemp)

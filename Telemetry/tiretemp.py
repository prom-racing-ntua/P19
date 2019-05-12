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
from customcolor import CustomColor

# Builder.load_string('''
# <TiretempLbl>:
#     Label:
#         size_hint: self.width,self.height
#         pos_hint: {'x': .8, 'y': .5}
#         canvas.before:
#             Rotate:
#                 angle: 45
#                 origin: self.center
#                 canvas.after:
#
#
# ''')



class TiretempLbl(SectorLabel) :
    lblname = StringProperty ()
    temptsur = NumericProperty()
    mintemp = NumericProperty ()
    maxtemp = NumericProperty ()


    def __init__(self, **kwargs):
        super(TiretempLbl,self).__init__ (**kwargs)
        print ("mphka super __init__ tire")
        self.templbl = SectorLabel(text = str(self.temptsur), color = [1,1,1,1] , bgclr = [0,0,0,0], font_size = '18sp')
        self.add_widget(self.templbl)

        self.bind(pos = self._update)
        self.bind(size = self._update)
        self.bind(temptsur = self._upgrade)


    def _update(self, *args):
        self.center = self.center_x, self.center_y
        self.size = self.size[0],self.size[1]
        self.lineclr = [1,1,1,1]

        print ('mphka update tire temp')

    def _upgrade (self, *args):
        texttemp = str (self.temptsur)
        self.templbl.text = texttemp[0:2]
        print ('mphka upgrade tiretemp')
        print (texttemp[0:2])
        print (self.templbl.color)
        # self.templbl.bgclr = self.customclr[index]
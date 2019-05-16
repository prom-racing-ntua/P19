#tiretemp
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



class TiretempLbl(GridLayout) :
    lblname = StringProperty ()
    xhint = NumericProperty()
    yhint = NumericProperty()
    xsize = NumericProperty()
    ysize = NumericProperty()
    temps = ListProperty([])
    customcolors = ListProperty([])
    floatcolor = ListProperty([])
    colors = ListProperty([])
    channel = ListProperty (['channel1','channel2','channel3','channel4','channel5','channel6','channel7',
                                'channel8','channel9','channel10','channel11','channel12','channel13','channel14',
                                'channel15','channel16'])


    def __init__(self, **kwargs):
        super(TiretempLbl,self).__init__ (**kwargs)
        self.cols=2
        self.rows=2
        self.spacing = 1.5
        # print ("mphka super __init__ tire")
        self.fl = BoxLayout(orientation = 'horizontal')
        self.fr = BoxLayout(orientation = 'horizontal')
        self.rl = BoxLayout(orientation = 'horizontal')
        self.rr = BoxLayout(orientation = 'horizontal')

        self.add_widget(self.fl)
        self.add_widget(self.fr)
        self.add_widget(self.rl)
        self.add_widget(self.rr)

        # for i,x in enumerate(self.children):
        #     print (i)
        #add labels
        for x in self.children:
            for y in range(1,5):
                x.add_widget(SectorLabel(text = 'hi',lineclr = [0,0,0,0],font_size = '16sp',color = [1,1,1,1]))

        # print (self.children[0].children)
        self.bind(pos = self._update)
        self.bind(size = self._update)
        self.bind(temps = self._upgrade)

        rgbfile = open('rgbvalues.txt') # Open file on read mode
        self.customcolor = rgbfile.read().split("\n") # Create a list containing all lines
        rgbfile.close() # Close file
        # print(self.customcolor)
        #split each element at ',' and add it in a new list
        for i in self.customcolor[0:99]:
            x= i.split(',')
            for y in x:
                self.floatcolor.append(float(y))
        # print (self.floatcolor)
        #configure each value at 0-1
        for i in range(296):
            self.floatcolor[i] = self.floatcolor[i]/255.0
        #put each element back at triades
        for i in range(0,296,3):
            self.colors.append(self.floatcolor[i:i+3])
            print (self.floatcolor[i:i+3])
        #add opacity
        for i in self.colors:
            i.append(float(0.5))
        print('########## COLORS ##########')
        print(self.colors)
        print('## LENGTH ##')
        print (len(self.colors))

    def _update(self,*args):
        self.pos= [self.x,self.y]
        self.size = (self.size[0],self.size[1])
        print('eimai update')
        print(self.x,self.y)
        print (self.size)
        # for x in self.children:
        #      for y in x.children:
        #          y.pos = 40,70
        #          y.size =20,50# self.size[0],self.size[1]

    def _upgrade(self,*args):
        print ('mphka _upgrade tiretemp')
        index = 0
        for x in self.children:
            for y in x.children:
                y.text = str(self.temps[index])
                print('---- '+str(index)+' ----')
                print(y.text)
                y.bgclr = self.colors[int(self.temps[index])]
                print(y.bgclr)
                index = index+1




    #     self.bind(pos=self._update)
    #     self.bind(size=self._update)
    #     self.bind(temps=self._upgarde)  ##update temp and color in each channel
    #
    # def _update(self,*args):
    #     self.
    #
    #
    # def _upgrade(self,*args):
    #     self.fl.

    # def _update(self, *args):
    #     self.templbl.center = self.center_x, self.center_y
    #     self.size = self.size[0],self.size[1]
    #     self.lineclr = [1,1,1,1]
    #
    #     # print ('mphka update tire temp')
    #
    # def _upgrade (self, *args):
    #     texttemp = str (self.temptsur)
    #     self.templbl.text = texttemp[0:2]
    #     # self.templbl.color = self.customcolors[int(self.temptsur)]
    #     # print ('mphka upgrade tiretemp')
    #     # print (texttemp[0:2])
    #     # print (self.templbl.color)
    #     # print (self.temptsur)
    #     # self.templbl.bgclr = self.customclr[index]
    #
    # def customColor (self,*args):
    #     rgbfile = open('rgbvalues.txt') # Open file on read mode
    #     lines = rgbfile.read().split("\n") # Create a list containing all lines
    #     customcolor = lines
    #     print (customcolor)
    #     rgbfile.close() # Close file
    #     self.customcolors = customcolor
    #     print (self.customcolors)

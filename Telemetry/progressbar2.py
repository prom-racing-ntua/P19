import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty,StringProperty, ListProperty,BoundedNumericProperty
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from sectorLabel import SectorLabel

class ProgressBar2 (Widget) :
    bgclr = ListProperty ([])
    lowclr1 = ListProperty ([])
    lowclr2 = ListProperty ([])
    lowclr3 = ListProperty ([])
    lowclr4 = ListProperty ([])
    lowclr5 = ListProperty ([])
    lowclr6 = ListProperty ([])
    med1clr1 = ListProperty ([])
    med1clr2 = ListProperty ([])
    med1clr3 = ListProperty ([])
    med1clr4 = ListProperty ([])
    med1clr5 = ListProperty ([])
    med1clr6 = ListProperty ([])
    med2clr1 = ListProperty ([])
    med2clr2 = ListProperty ([])
    med2clr3 = ListProperty ([])
    highclr1 = ListProperty ([])
    highclr2 = ListProperty ([])
    highclr3 = ListProperty ([])
    progresslvl = BoundedNumericProperty (0,min=0,max=12,errorvalue=12)
    anglestart = NumericProperty ()
    anglestop = NumericProperty ()


    def __init__ (self,**kwargs):
        super (ProgressBar2,self).__init__(**kwargs)
        print ("mphka super __init__")
        print (self.anglestart)
        print (self.anglestart+(self.progresslvl*10))
        for i in range(self.anglestop-self.anglestart):
            Builder.load_string ('''
            <ProgressBarakuda>
                canvas:
                    Color :
                        rgba: [1,0,0,1]
                    Line :
                        id : testline
                        width : 2
                        ellipse : (self.x, self.y, self.width-80 , self.height+160 , self.anglestart+i, self.anglesart+(progresslvl*10))
            ''')

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

Builder.load_string('''
<ProgressBa>:
    canvas:
        ## basic slim red line
        Color:
            rgba: [1,0,0,1] if self.progresslvl == 0 else [1,0,0,0]
        Line:
            id : linebase
            width: 1
            ellipse: (self.x, self.y, self.width-80, self.height+160, self.anglestart,self.anglestop)

        ## first step lines (yellow) - low
        ## line 1/3
        Color:
            rgba : self.lowclr1 if (self.progresslvl > 0) else [1,0,0,1]
        Line:
            id : lowline1
            width : 2.2 if (self.progresslvl > 0) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart,self.anglestart+(self.progresslvl*10))
        ## line 2/3
        Color:
            rgba : self.lowclr2 if (self.progresslvl > 1) else [1,0,0,1]
        Line:
            id : lowline2
            width : 3.4 if (self.progresslvl > 1) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+10,self.anglestart+(self.progresslvl*10))
        ## line 3/3
        Color:
            rgba : self.lowclr3 if (self.progresslvl > 2) else [1,0,0,1]
        Line:
            id : lowline3
            width : 4.8 if (self.progresslvl > 2) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+20,self.anglestart+(self.progresslvl*10))


        ## second step lines (green) - medium 1
        ## line 1/3
        Color:
            rgba : self.med1clr1 if (self.progresslvl > 3) else [1,0,0,1]
        Line:
            id : med1line1
            width : 6.2  if (self.progresslvl > 3) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+30,self.anglestart+(self.progresslvl*10))
        ## med line 2/3
        Color:
            rgba : self.med1clr2 if (self.progresslvl > 4) else [1,0,0,1]
        Line:
            id : med1line2
            width : 8.2  if (self.progresslvl > 4) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+40,self.anglestart+(self.progresslvl*10))
        ## med line 3/3
        Color:
            rgba : self.med1clr3 if (self.progresslvl > 5) else [1,0,0,1]
        Line:
            id : med1line3
            width : 10.6  if (self.progresslvl > 5) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+50,self.anglestart+(self.progresslvl*10))

        ## third step lines (blue) - medium 2
        ## med2 line 1/3
        Color:
            rgba : self.med2clr1 if (self.progresslvl > 6) else [1,0,0,1]
        Line:
            id : med2line1
            width : 13.2 if (self.progresslvl > 6) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+60,self.anglestart+(self.progresslvl*10))
        ## med2 line 2/3
        Color:
            rgba : self.med2clr2 if (self.progresslvl > 7) else [1,0,0,1]
        Line:
            id : med2line1
            width : 16 if (self.progresslvl > 7) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+70,self.anglestart+(self.progresslvl*10))
        ## med2 line 3/3
        Color:
            rgba : self.med2clr3 if (self.progresslvl > 8) else [1,0,0,1]
        Line:
            id : med2line3
            width : 19 if (self.progresslvl > 8) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+80,self.anglestart+(self.progresslvl*10))

        ## fourth step lines (red) - high
        ## high line 1/2
        Color:
            rgba : self.highclr1 if (self.progresslvl > 9) else [1,0,0,1]
        Line:
            id : highline1
            width : 21 if (self.progresslvl > 9) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+90,self.anglestart+(self.progresslvl*10))
        ## high line 2/2
        Color:
            rgba : self.highclr2 if (self.progresslvl > 10) else [1,0,0,1]
        Line:
            id : highline2
            width : 22.4 if (self.progresslvl > 10) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+100,self.anglestart+(self.progresslvl*10))
        ## high line 3/3 - end
        Color:
            rgba : self.highclr2 if (self.progresslvl > 10) else [1,0,0,1]
        Line:
            id : highline2
            width : 22.4 if (self.progresslvl > 10) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+100,self.anglestart+(self.progresslvl*10))

    Label:
        id : rpm2k
        text : 'rpm'


''')

class ProgressBa (Widget) :
    bgclr = ListProperty ([])
    lowclr1 = ListProperty ([])
    lowclr2 = ListProperty ([])
    lowclr3 = ListProperty ([])
    med1clr1 = ListProperty ([])
    med1clr2 = ListProperty ([])
    med1clr3 = ListProperty ([])
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
        super (ProgressBa,self).__init__(**kwargs)
        print ("mphka super __init__")
        print (self.anglestart)
        print (self.anglestart+(self.progresslvl*10))

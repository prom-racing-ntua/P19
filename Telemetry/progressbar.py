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
        ## line 1/6
        Color:
            rgba : self.lowclr1 if (self.progresslvl > 0) else [1,0,0,1]
        Line:
            id : lowline1
            width : 1.6 if (self.progresslvl > 0) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart,self.anglestart+(self.progresslvl*10))
        ## line 2/6
        Color:
            rgba : self.lowclr2 if (self.progresslvl > 0.5) else [1,0,0,1]
        Line:
            id : lowline2
            width : 2.2 if (self.progresslvl > 0.5) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+5,self.anglestart+(self.progresslvl*10))
        ## line 3/6
        Color:
            rgba : self.lowclr3 if (self.progresslvl > 1) else [1,0,0,1]
        Line:
            id : lowline3
            width : 2.8 if (self.progresslvl > 1) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+10,self.anglestart+(self.progresslvl*10))
        ## line 4/6
        Color:
            rgba : self.lowclr4 if (self.progresslvl > 1.5) else [1,0,0,1]
        Line:
            id : lowline4
            width : 3.4 if (self.progresslvl > 1.5) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+15,self.anglestart+(self.progresslvl*10))
        ## line 5/6
        Color:
            rgba : self.lowclr5 if (self.progresslvl > 2) else [1,0,0,1]
        Line:
            id : lowline5
            width : 4 if (self.progresslvl > 2) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+20,self.anglestart+(self.progresslvl*10))
        ## line 6/6
        Color:
            rgba : self.lowclr6 if (self.progresslvl > 2.5) else [1,0,0,1]
        Line:
            id : lowline6
            width : 4.6 if (self.progresslvl > 2.5) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+25,self.anglestart+(self.progresslvl*10))


        ## second step lines (green) - medium 1
        ## med line 1/6
        Color:
            rgba : self.med1clr1 if (self.progresslvl > 3) else [1,0,0,1]
        Line:
            id : med1line1
            width : 5.3  if (self.progresslvl > 3) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+30,self.anglestart+(self.progresslvl*10))
        ## med line 2/6
        Color:
            rgba : self.med1clr2 if (self.progresslvl > 3.5) else [1,0,0,1]
        Line:
            id : med1line2
            width : 6.1  if (self.progresslvl > 3.5) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+35,self.anglestart+(self.progresslvl*10))
        ## med line 3/6
        Color:
            rgba : self.med1clr3 if (self.progresslvl > 4) else [1,0,0,1]
        Line:
            id : med1line3
            width : 6.9  if (self.progresslvl > 4) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+40,self.anglestart+(self.progresslvl*10))
        ## med line 4/6
        Color:
            rgba : self.med1clr4 if (self.progresslvl > 4.5) else [1,0,0,1]
        Line:
            id : med1line4
            width : 7.7  if (self.progresslvl > 4.5) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+45,self.anglestart+(self.progresslvl*10))
        ## med line 5/6
        Color:
            rgba : self.med1clr5 if (self.progresslvl > 5) else [1,0,0,1]
        Line:
            id : med1line5
            width : 8.5  if (self.progresslvl > 5) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+50,self.anglestart+(self.progresslvl*10))
        ## med line 6/6
        Color:
            rgba : self.med1clr6 if (self.progresslvl > 5.5) else [1,0,0,1]
        Line:
            id : med1line6
            width : 9.3  if (self.progresslvl > 5.5) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+55,self.anglestart+(self.progresslvl*10))


        ## third step lines (blue) - medium 2
        ## med2 line 1/12
        Color:
            rgba : self.med2clr1 if (self.progresslvl > 6) else [1,0,0,1]
        Line:
            id : med2line1
            width : 10.1 if (self.progresslvl > 6) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+60,self.anglestart+(self.progresslvl*10))
        ## med2 line 2/12
        Color:
            rgba : self.med2clr2 if (self.progresslvl > 6.25) else [1,0,0,1]
        Line:
            id : med2line2
            width : 10.55 if (self.progresslvl > 6.25) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+62.5,self.anglestart+(self.progresslvl*10))

        ## med2 line 3/12
        Color:
            rgba : self.med2clr3 if (self.progresslvl > 6.5) else [1,0,0,1]
        Line:
            id : med2line3
            width : 11 if (self.progresslvl > 6.5) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+65,self.anglestart+(self.progresslvl*10))

        ## med2 line 4/12
        Color:
            rgba : self.med2clr4 if (self.progresslvl > 6.75) else [1,0,0,1]
        Line:
            id : med2line4
            width : 11.45 if (self.progresslvl > 6.75) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+67.5,self.anglestart+(self.progresslvl*10))

        ## med2 line 5/12
        Color:
            rgba : self.med2clr5 if (self.progresslvl > 7) else [1,0,0,1]
        Line:
            id : med2line5
            width : 12 if (self.progresslvl > 7) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+70,self.anglestart+(self.progresslvl*10))
        ## med2 line 6/12
        Color:
            rgba : self.med2clr6 if (self.progresslvl > 7.25) else [1,0,0,1]
        Line:
            id : med2line6
            width : 12.5 if (self.progresslvl > 7.25) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+72.5,self.anglestart+(self.progresslvl*10))
        ## med2 line 7/12
        Color:
            rgba : self.med2clr7 if (self.progresslvl > 7.5) else [1,0,0,1]
        Line:
            id : med2line7
            width : 13 if (self.progresslvl > 7.5) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+75,self.anglestart+(self.progresslvl*10))

        ## med2 line 8/12
        Color:
            rgba : self.med2clr8 if (self.progresslvl > 7.75) else [1,0,0,1]
        Line:
            id : med2line8
            width : 13.5 if (self.progresslvl > 7.75) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+77.5,self.anglestart+(self.progresslvl*10))

        ## med2 line 9/12
        Color:
            rgba : self.med2clr9 if (self.progresslvl > 8) else [1,0,0,1]
        Line:
            id : med2line9
            width : 14 if (self.progresslvl > 8) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+80,self.anglestart+(self.progresslvl*10))

        ## med2 line 10/12
        Color:
            rgba : self.med2clr10 if (self.progresslvl > 8.25 ) else [1,0,0,1]
        Line:
            id : med2line10
            width : 14.5 if (self.progresslvl > 8.25) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+82.5,self.anglestart+(self.progresslvl*10))

        ## med2 line 11/12
        Color:
            rgba : self.med2clr11 if (self.progresslvl > 8.5) else [1,0,0,1]
        Line:
            id : med2line11
            width : 15 if (self.progresslvl > 8.5) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+85,self.anglestart+(self.progresslvl*10))

        ## med2 line 12/12
        Color:
            rgba : self.med2clr12 if (self.progresslvl > 8.75) else [1,0,0,1]
        Line:
            id : med2line12
            width : 15.5 if (self.progresslvl > 8.75) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+87.5,self.anglestart+(self.progresslvl*10))


        ## fourth step lines (red) - high
        ## high line 1/3
        Color:
            rgba : self.highclr1 if (self.progresslvl > 9) else [1,0,0,1]
        Line:
            id : highline1
            width : 15.7 if (self.progresslvl > 9) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+90,self.anglestart+(self.progresslvl*10))
        ## high line 2/3
        Color:
            rgba : self.highclr2 if (self.progresslvl > 9.5) else [1,0,0,1]
        Line:
            id : highline2
            width : 16.8 if (self.progresslvl > 9.5) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+95,self.anglestart+(self.progresslvl*10))
        ## high line 3/3 - end
        Color:
            rgba : self.highclr2 if (self.progresslvl > 10) else [1,0,0,1]
        Line:
            id : highline2
            width : 18 if (self.progresslvl > 10) else 1
            ellipse : (self.x,self.y,self.width-80 , self.height+160, self.anglestart+100,self.anglestart+(self.progresslvl*10))

''')

class ProgressBa (Widget) :
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
    med2clr4 = ListProperty ([])
    med2clr5 = ListProperty ([])
    med2clr6 = ListProperty ([])
    med2clr7 = ListProperty ([])
    med2clr8 = ListProperty ([])
    med2clr9 = ListProperty ([])
    med2clr10 = ListProperty ([])
    med2clr11 = ListProperty ([])
    med2clr12 = ListProperty ([])
    highclr1 = ListProperty ([])
    highclr2 = ListProperty ([])
    highclr3 = ListProperty ([])
    progresslvl = BoundedNumericProperty (0,min=0,max=12,errorvalue=12)
    anglestart = NumericProperty ()
    anglestop = NumericProperty ()
    rpmlvl = StringProperty()


    def __init__ (self,**kwargs):
        super (ProgressBa,self).__init__(**kwargs)
        print ("mphka super __init__ progresssbarr")
        print (self.anglestart)
        print (self.anglestart+(self.progresslvl*10))

        self.progresslabel = Label(font_size='30sp')
        self.rpmlabel = Label(text = 'RPM',font_size='10sp')
        self.add_widget(self.progresslabel)
        self.add_widget(self.rpmlabel)
        self.bind(pos = self._update)
        self.bind(size = self._update)
        self.bind(progresslvl = self._upgrade)

    def _update(self,*args):
        self.progresslabel.pos = self.x,self.center_y+1.5*self.height
        self.progresslabel.size = self.size[0]/10,self.size[1]/10
        self.rpmlabel.pos = self.x,self.center_y+1.5*self.height-20
        self.rpmlabel.size = self.size[0]/10,self.size[1]/10

    def _upgrade(self,*args):
        self.rpmlvl = str(self.progresslvl*1000)
        self.progresslabel.text = self.rpmlvl[0:4]
        self.progresslabel.color = [1,0,0,1]

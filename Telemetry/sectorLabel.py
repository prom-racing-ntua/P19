#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from kivy.uix.image import Image
from hover import HoverBehavior

from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty,ListProperty


Builder.load_string('''
<SectorLabel>:
    id: self.name
    canvas:
        Color:
            rgba: self.bgclr
        Rectangle:
            pos: self.x, self.y
            size: self.size
        Color:
            rgba: self.lineclr
        Line:
            rectangle: self.x,self.y,self.width,self.height
            width: 1
''')
#binding pos and size with the update method does not affect
#rectangles position, so its gonna be in different position

class SectorLabel(Label,Widget):
    name = StringProperty()
    lineclr = ListProperty([])
    bgclr = ListProperty([])
    def __init__(self,bgclr=None,lineclr=None,**kwargs):
        self.lineclr = lineclr if lineclr is not None  else [1,0,0,0.1]
        self.bgclr = bgclr if bgclr is not None else [1,1,1,0]
        super(SectorLabel, self).__init__(**kwargs)

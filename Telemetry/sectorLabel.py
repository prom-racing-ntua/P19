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
    canvas:
        Color:
            rgba: [1,1,1,0.1]
        Rectangle:
            pos: self.x, self.y
            size: self.size
        Color:
            rgba: self.bgclr
        Line:
            rectangle: self.x,self.y,self.width,self.height
            width: 1
''')

class SectorLabel(Label,Widget):
	bgclr = ListProperty([1,1,1,0.1])
	def __init__(self, bgclr, **kwargs):
		self.bgclr=bgclr
		super(SectorLabel, self).__init__(**kwargs)


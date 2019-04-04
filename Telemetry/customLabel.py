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
<CustomLabel>:
    canvas:
        Color:
            rgba: [1,1,1,0]
        Rectangle:
            pos: self.x+self.font_size if self.font_size<=13 else self.x, self.y+self.size[1]/3
            size: self.font_size*6,self.size[1]/3
        Color:
            rgba: self.bgclr
        Line:
            rectangle: self.x+self.font_size if self.font_size<=13 else self.x,self.y+self.height/3,self.font_size*6,self.height/3
            width: 1
''')

class CustomLabel(Label,Widget):
	bgclr = ListProperty([1,1,1,0.1])
	def __init__(self, bgclr, **kwargs):
		self.bgclr=bgclr
		super(CustomLabel, self).__init__(**kwargs)


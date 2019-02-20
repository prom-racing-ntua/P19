#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from hover import HoverBehavior

from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty


Builder.load_string('''
<TestWidget>:
    canvas:
        Color:
            rgba: [0.22,0.345,0.265,1] if self.hovered else [0.12,0.145,0.165,1]
        Rectangle:
            pos: self.center_x-self.size[0]/2, self.center_y-self.size[1]/2
            size: self.size
        Color:
            rgba: [1,1,1,1]
        Line:
            rectangle: self.x,self.y,self.width,self.height
            width: 2
''')

class TestWidget(Widget,HoverBehavior):
    value = StringProperty("TEST")
    size_text = StringProperty('20sp')
    #variables representing all possible values' states
    limit_value = int(200)
    dangerous = BooleanProperty(False)
    critical = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(TestWidget, self).__init__(**kwargs)

        self.message=Label(
            text= self.value,
            font_size='30sp'
            )

        self.add_widget(self.message)
        self.bind(pos = self._shape)
        self.bind(size = self._shape)
        self.bind(value = self._val)
        #if value -> dangerous we want widget background to be red
        if self._is_dangerous:
            self.bind(self._danger)


    def _shape(self, *args):
        self.message.center = (self.center_x, self.center_y)

    def _val(self, *args):
        self.message.text = self.value

    #check and set darnegrous variable
    #return it for the if statenment
    def _is_dangerous(self, *args):
        if int(self.limit_value) >= int (self.value):
            self.dangerous = BooleanProperty(True)
        return self.dangerous

    #set the background color of the widget
    def _danger(self, *args):
        self.color = (1,0,0,1)

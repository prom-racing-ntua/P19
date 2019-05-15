#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.properties import NumericProperty,StringProperty,BoundedNumericProperty,ListProperty
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from os.path import join, dirname, abspath
import os

class Accel(Widget):

    unit = NumericProperty(1)
    value=ListProperty ([0,0])
    path = os.getcwd()
    file_backgnd = StringProperty(join(path, "./Images/scope.png" ))
    file_point = StringProperty(join(path, "./Images/point_gg.png" ))
    size_backgnd = BoundedNumericProperty(128, min=128, max=256, errorvalue=128)
    size_text = NumericProperty(10)
    widget_name=StringProperty()
    widget_unit=StringProperty()
    def __init__(self, **kwargs):
        super(Accel, self).__init__(**kwargs)


        self._img_backgnd = Image(
            source=self.file_backgnd,
            size=(self.size_backgnd, self.size_backgnd)
        )

        self._img_point = Image(
            source=self.file_point,
            size=(self.size_backgnd, self.size_backgnd)
        )

        self._labelunit = Label(text=self.widget_unit,font_size=self.size_text-3)
        self._glab = Label(font_size=self.size_text, markup=True)

        self.add_widget(self._img_backgnd)
        self.add_widget(self._img_point)
        self.add_widget(self._glab)
        self.add_widget(self._labelunit)
        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(value=self._turn)

    def _update(self, *args):
        print("hellloooooooooo!")
        self._img_backgnd.pos = self.x,self.y
        self._img_backgnd.size = self.size[0],self.size[1]
        self._img_backgnd.center = self.center_x,self.center_y
        self._labelunit.center = (self._img_backgnd.center_x,self._img_backgnd.center_y-(self.size_backgnd/4))
        self._glab.center= (self._img_backgnd.center_x,self._img_backgnd.y)
        self._img_point.center = self.center_x,self.center_y

    def _turn(self, *args):
        print ('mphka gg turn')
        self._img_point.center=(self._img_backgnd.center_x+(self.value[0]>>9)*1.5,self._img_backgnd.center_y+(self.value[1]>>9)*1.5)
        self._glab.text = "Lat: "+str(round((self.value[0]/9806),1))+"/ Long: "+str(round((self.value[1]/9806),1))

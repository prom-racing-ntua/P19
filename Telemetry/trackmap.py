#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kivy,math
kivy.require('1.10.0')
from kivy.properties import NumericProperty,StringProperty,ListProperty,BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color,Line
from kivy.lang import Builder
from kivy.uix.image import Image

ccc=math.cos(math.radians(46.894893))
earth_radius=6367116


Builder.load_string('''
<TrackMap>:
    id: me
    canvas:
        Color:
            rgba: self.color0
        Line:
            points: self.points_sec0
            width: self.wid
        Line:
            points: me.calculate_vertical(self.points_sec0[0:4])
            width: self.wid
        Color:
            rgba: self.color1
        Line:
            points: self.points_sec1
            width: self.wid
        Line:
            points: me.calculate_vertical(self.points_sec1[0:4])
            width: self.wid
        Color:
            rgba: self.color2
        Line:
            points: self.points_sec2
            width: self.wid
        Line:
            points: me.calculate_vertical(self.points_sec2[0:4])
            width: self.wid
    Image:
        source: "./Images/point.png"
        size: 10,10
        pos: me.cooked_coords[0]-5,me.cooked_coords[1]-5
    ''')
class TrackMap(Widget):
    color0 = ListProperty([0,1,0,1])
    color1 = ListProperty([1,0,1,1])
    color2 = ListProperty([1,1,0,1])
    map_file = StringProperty("track.txt")
    xmin = NumericProperty(0)
    ymin = NumericProperty(0)
    wid = NumericProperty(2)
    points_sec0 = ListProperty([1,2,1,3])
    points_sec1 = ListProperty([1,2,1,3])
    points_sec2 = ListProperty([1,2,1,3])
    scale = NumericProperty(4)
    po = []
    cooked_coords=ListProperty([5,5])
    raw_coords=ListProperty([5,5])
    def __init__(self, **kwargs):
        super(TrackMap, self).__init__(**kwargs)
        file = open(self.map_file,"r")
        x = []
        y = []
        sect = []
        for line in file:
            temp=line.split(',')
            x.append(earth_radius*math.radians(float(temp[1]))*ccc)
            y.append(earth_radius*math.radians(float(temp[0])))
            sect.append(int(temp[2]))
        file.close()
        minx=min(x)
        self.xmin=minx
        miny=min(y)
        self.ymin=miny
        maxx=max(x)
        maxy=max(y)
        self.points_sec0=[]
        self.points_sec1=[]
        self.points_sec2=[]

        self.scale = max(self.width/(maxx-minx)*1.8,self.height/(maxy-miny)*1.8)
        for i in range(len(x)):
            if sect[i]==0:
                self.points_sec0.append((x[i]-minx)*self.scale)
                self.points_sec0.append((y[i]-miny)*self.scale)
            elif sect[i]==1:
                self.points_sec1.append((x[i]-minx)*self.scale)
                self.points_sec1.append((y[i]-miny)*self.scale)
            else:
                self.points_sec2.append((x[i]-minx)*self.scale)
                self.points_sec2.append((y[i]-miny)*self.scale)
        self.bind(raw_coords=self.change_pos)
    def change_pos(self, *args):
        self.cooked_coords[0] = (earth_radius*math.radians(float(self.raw_coords[1]))*ccc-self.xmin)*self.scale
        self.cooked_coords[1] = (earth_radius*math.radians(float(self.raw_coords[0]))-self.ymin)*self.scale
    def calculate_vertical(self,two_points):
        x1=two_points[0]
        y1=two_points[1]
        x2=two_points[2]
        y2=two_points[3]
        a=(x1-x2)/(y1-y2)
        b=y1-a*x1
        return(x1+2,b+a*(x1+2),x1-2,b+a*(x1-2))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')
from kivy.config import Config
Config.set('graphics', 'width', str(1200))
Config.set('graphics', 'height', str(700))
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line,Color
from kivy.uix.image import Image
from kivy.garden.graph import Graph, LinePlot, MeshLinePlot
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.slider import Slider
from datetime import datetime
import serial,time,math,random,queue

from test import TestWidget


def convert(clat,clon):    ##convert gps coords
	# 3804.1712,02348.9058
	lat=int(clat[0:2])+round(float(clat[2:9])/60,6)
	lon=int(clon[0:3])+round(float(clon[3:10])/60,6)
	return lat,lon

if __name__ == '__main__':
	# ser = serial.Serial('COM3',115200)   ##(for windows)
	# ser = serial.Serial('/dev/ttyACM0',115200)  ##(for linux)
	class TelemetryApp(App):
		i = 0
		def build(self):
			Window.clearcolor = (85/256,23/256,23/256,1)
			Window.fullscreen = False
			main_window = FloatLayout()
			main_window.add_widget(
				Image(
					source= "Images/NTUA.png",
					pos_hint= {'x':0.1,'y':0.8},
					size_hint= (0.8,0.2)
				)
			)
			main_window.add_widget(
				Label(
					text= "NTU Athens",
					font_size= '40sp',
					color= (1,1,0,1),
					pos_hint= {'x':0.1,'y':0.4},
					size_hint= (0.8,0.2)
				)
			)
			main_window.add_widget(
				TestWidget(
					value= 20,
					pos_hint= {'x':0,'y':0.8},
					size_hint= (0.3,0.2)
				)
			)
			main_window.add_widget(
				TestWidget(
					value= 201,
					pos_hint= {'x':0,'y':0.45},
					size_hint= (0.3,0.35)
				)
			)
			self.a=TestWidget(
					value= 27,
					pos_hint= {'x':0,'y':0.2},
					size_hint= (0.3,0.25)

				)
			main_window.add_widget(
				TestWidget(
					value= 20,
					pos_hint= {'x':0,'y':0},
					size_hint= (0.3,0.2)
				)
			)
			main_window.add_widget(self.a)
			# self.a.value = "dwhkhdwh"
			Clock.schedule_interval(lambda *t: self.get_data(), 0.01)
			return main_window
		def get_data(self):
			#received_data = ser.read()
			self.i+=1
			self.a.value=str(self.i)
			#we set the limit_value so we can check if its dangerous
			self.a.limit_value = 200
			#self.a.is_dangerous()
	try:
		TelemetryApp().run()
	except Exception as e:
		# ser.close()
		raise e




##test

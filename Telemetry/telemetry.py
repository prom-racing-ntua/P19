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
from kivy.garden.graph import LinePlot, MeshLinePlot
from customGraph import Graph
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.slider import Slider
from datetime import datetime
import serial,time,math,random,queue,numpy
from collections import deque


from test import TestWidget
from graph_widgets import *

def convert(clat,clon):    ##convert gps coords
	# 3804.1712,02348.9058
	lat=int(clat[0:2])+round(float(clat[2:9])/60,6)
	lon=int(clon[0:3])+round(float(clon[3:10])/60,6)
	return lat,lon


if __name__ == '__main__':
	# ser = serial.Serial('COM3',115200)   ##(for windows)
	# ser = serial.Serial('/dev/ttyACM0',115200)  ##(for linux)
	ax_list=deque(maxlen=300)
	ay_list=deque(maxlen=300)
	brake=deque(maxlen=300)
	tps=deque(maxlen=300)

	class TelemetryApp(App):
		i = 0
		def build(self):
			Window.clearcolor = (0,0,0,1)
			Window.fullscreen = False
			Clock.schedule_interval(lambda *t: self.get_data(), 0.016)
			main_window.add_widget(
					TestWidget(
						value=30,
						pos_hint={'x':0,'y':0.8},
						size_hint=(0.3,0.2)
					))
			main_window.add_widget(
					TestWidget(
						value=30,
						pos_hint={'x':0,'y':0.5},
						size_hint=(0.3,0.3)
					))
			return main_window
		def get_data(self):
			ax_list.append((self.i,math.sin(2*math.pi*self.i)))
			ay_list.append((self.i,math.sin(2*math.pi*self.i)))
			brake.append((self.i,23+10*math.sin(2*math.pi*self.i)))
			tps.append((self.i,44-10*math.sin(2*math.pi*self.i)))

			ax_plot.points=ax_list
			ay_plot.points=ay_list
			brake_plot.points=brake
			tps_plot.points=tps
			brake_tps_steering.xmax = gear_rpm_speed.xmax = accel_x.xmax = accel_y.xmax = self.i
			brake_tps_steering.xmin = gear_rpm_speed.xmin = accel_x.xmin = accel_y.xmin = self.i-4
			self.i+=0.016
	try:
		TelemetryApp().run()
	except Exception as e:
		# ser.close()
		raise e




##test

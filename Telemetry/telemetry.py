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
from sectors import Sectors
from center import *
from left import *
from right import *
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
			Window.clearcolor = (0,0,0,1)
			Window.fullscreen = False
			main_window=FloatLayout()
			Clock.schedule_interval(lambda *t: self.get_data(), 0.016)
			main_window.add_widget(left_column)
			main_window.add_widget(center_column)
			main_window.add_widget(right_column)
			return main_window
		def get_data(self):
			accel_x.points_list_t[0].append((self.i,math.sin(math.pi*self.i)))
			accel_y.points_list_t[0].append((self.i,math.sin(2*math.pi*self.i)/2))
			brake_tps_steering.points_list_t[0].append((self.i,math.sin(2*math.pi*self.i)))
			brake_tps_steering.points_list_t[1].append((self.i,2*math.sin(2*math.pi*self.i)))
			brake_tps_steering.points_list_t[2].append((self.i,20*math.sin(2*math.pi*self.i)))

			gear_rpm_speed.points_list_t[0].append((self.i,int(abs(5*math.sin(math.pi*self.i)))))
			gear_rpm_speed.points_list_t[1].append((self.i,math.sin(math.pi*self.i)))
			gear_rpm_speed.points_list_t[2].append((self.i,2*math.sin(math.pi*self.i)))

			roll_pitch.points_list_t[0].append((self.i,0.5*math.sin(math.pi*self.i)))
			roll_pitch.points_list_t[1].append((self.i,math.sin(math.pi*self.i)))
			roll_pitch.points_list_t[2].append((self.i,math.sin(2*math.pi*self.i)))

			shock_travel.points_list_t[0].append((self.i,12*math.sin(math.pi*self.i)))
			shock_travel.points_list_t[1].append((self.i,12+4*math.sin(math.pi*self.i)))
			shock_travel.points_list_t[2].append((self.i,20*math.sin(math.pi*self.i)))
			shock_travel.points_list_t[3].append((self.i,40*math.sin(math.pi*self.i)))

			accel_x.points_list_m[0].append((self.i,1.5*math.sin(math.pi*self.i)))
			accel_y.points_list_m[0].append((self.i,1.5*math.sin(2*math.pi*self.i)/2))
			brake_tps_steering.points_list_m[0].append((self.i,1.5*math.sin(2*math.pi*self.i)))
			brake_tps_steering.points_list_m[1].append((self.i,1.5*2*math.sin(2*math.pi*self.i)))
			brake_tps_steering.points_list_m[2].append((self.i,1.5*20*math.sin(2*math.pi*self.i)))

			gear_rpm_speed.points_list_m[0].append((self.i,1.5*int(abs(5*math.sin(math.pi*self.i)))))
			gear_rpm_speed.points_list_m[1].append((self.i,1.5*math.sin(math.pi*self.i)))
			gear_rpm_speed.points_list_m[2].append((self.i,1.5*2*math.sin(math.pi*self.i)))

			roll_pitch.points_list_m[0].append((self.i,1.5*0.5*math.sin(math.pi*self.i)))
			roll_pitch.points_list_m[1].append((self.i,1.5*math.sin(math.pi*self.i)))
			roll_pitch.points_list_m[2].append((self.i,1.5*math.sin(2*math.pi*self.i)))

			shock_travel.points_list_m[0].append((self.i,1.5*12*math.sin(math.pi*self.i)))
			shock_travel.points_list_m[1].append((self.i,1.5*12+4*math.sin(math.pi*self.i)))
			shock_travel.points_list_m[2].append((self.i,1.5*20*math.sin(math.pi*self.i)))
			shock_travel.points_list_m[3].append((self.i,1.5*40*math.sin(math.pi*self.i)))

			accel_x.change = accel_y.change = brake_tps_steering.change = gear_rpm_speed.change = roll_pitch.change = shock_travel.change = True
			accel_x.xmin = accel_y.xmin =gear_rpm_speed.xmin = brake_tps_steering.xmin = roll_pitch.xmin = shock_travel.xmin = self.i-4
			accel_x.xmax = accel_y.xmax =gear_rpm_speed.xmax = brake_tps_steering.xmax = roll_pitch.xmax = shock_travel.xmax = self.i
			self.i+=0.016

			##create each sector
			sector1.currenttime = str(self.i)
			#sector1.lap = int(self.i)
			sector2.currenttime = str(self.i/2)
			#sector2.lap = int (self.i)
			sector3.currenttime = str(self.i/10)
			#sector3.lap = int(self.i)
	try:
		TelemetryApp().run()
	except Exception as e:
		# ser.close()
		raise e




##test

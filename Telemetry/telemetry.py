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
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.slider import Slider
from datetime import datetime
import time,math,random,queue,numpy
from collections import deque
from datetime import *
from landingForm import LandingForm


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

file = open("track.txt","r")
temp = []
j=0
for line in file:
	temp.append((float(line.split(',')[0]),float(line.split(',')[1])))

if __name__ == '__main__':
	# ser = serial.Serial('COM3',115200)   ##(for windows)
	# ser = serial.Serial('/dev/ttyACM0',115200)  ##(for linux)
	class TelemetryApp(App):
		i = 0
		def build(self):
			Window.clearcolor = (0,0,0,1)
			Window.fullscreen = False
			main_window=FloatLayout()
			main_window.add_widget(left_column)
			main_window.add_widget(center_column)
			main_window.add_widget(right_column)

			popup = Popup(
					title='Telemetry Setup',
					content=Label(text="OPA"),
					pos_hint={'x':0.20,'y':0.1},
					size_hint=(0.6, 0.8))
			main_window.add_widget(popup)
			return main_window
		def get_data(self):
			accel_x.points_list_t[0].append((self.i,-4))
			accel_y.points_list_t[0].append((self.i,-4))

			brake_tps_steering.points_list_t[0].append((self.i,-2))
			brake_tps_steering.points_list_t[1].append((self.i,-2))
			brake_tps_steering.points_list_t[2].append((self.i,-2))

			gear_rpm_speed.points_list_t[0].append((self.i,-1))
			gear_rpm_speed.points_list_t[1].append((self.i,-1))
			gear_rpm_speed.points_list_t[2].append((self.i,-1))

			roll_pitch.points_list_t[0].append((self.i,-4))
			roll_pitch.points_list_t[1].append((self.i,-4))
			roll_pitch.points_list_t[2].append((self.i,-4))

			shock_travel.points_list_t[0].append((self.i,-32))
			shock_travel.points_list_t[1].append((self.i,-32))
			shock_travel.points_list_t[2].append((self.i,-32))
			shock_travel.points_list_t[3].append((self.i,-32))

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
			self.i+=0.016
			global j
			j+=0.5
			track_map.raw_coords=temp[int(j)%len(temp)]
			##create each sector
			sector1.currenttime = str(self.i)
			#sector1.lap = int(self.i)
			sector2.currenttime = str(self.i/2)
			#sector2.lap = int (self.i)
			sector3.currenttime = str(self.i/10)
			#sector3.lap = int(self.i)
			progress1.progresslvl = (1+math.sin(4*math.pi*self.i))*5
			# utclbl1.utctime = accel_x.points_list_t
			# utclbl1.utcdate = accel_y.points_list_t
			gearlbl.currentgear = 4
			speedlbl.currentspeed = 120
			# frontleft.temptsur = self.i
			# tpsgauge.tpsvalue = self.i*500
			# brakegauge.brakevalue = self.i*500
			testtemp.temps = [10,20,30,40,45,55,60,65,70,75,80,85,90,95,96,98]
			gg_diagram.value = [1,1]
	try:
		TelemetryApp().run()
	except Exception as e:
		# ser.close()
		file.close()

		raise e

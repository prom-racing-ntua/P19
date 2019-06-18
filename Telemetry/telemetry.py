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
from popupwidget import PopupWidget


from test import TestWidget
from sectors import Sectors
from center import *
from left import *
from right import *
import serial

# ser = serial.Serial()
# print(ser.name)

streamline = list()
for i in range(65):
	streamline.append(0)

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
					content = PopupWidget(),
					confirm = Button(text = 'confirm',pos_hint={'x':0.5,'y':0.15}),
					pos_hint={'x':0.20,'y':0.1},
					size_hint=(0.6, 0.8))
			confirm.bind(on_press= popup.dismiss)
			main_window.add_widget(popup)
			print (popup.content.children)`
			++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++	--`
			Clock.schedule_interval(lambda *t: self.get_data(), 0.01)
			return main_window
		def get_data(self):
			global streamline
			# if ser.in_waiting:
			# 	mydata = str(ser.readline()).split("'")[1].split('\\')[0].split(',')
			# 	streamline = [int(x) for x in mydata]

			accel_x.points_list_t[0].append((streamline[0],streamline[10]))
			accel_y.points_list_t[0].append((streamline[0],streamline[11]))

			brake_tps_steering.points_list_t[0].append((streamline[0],(streamline[41]-streamline[40])/2)) ##### metatroph### check
			brake_tps_steering.points_list_t[1].append((streamline[0],streamline[16]))
			brake_tps_steering.points_list_t[2].append((streamline[0],streamline[63]))# metatroph

			gear_rpm_speed.points_list_t[0].append((streamline[0],streamline[15]))#gear
			gear_rpm_speed.points_list_t[1].append((streamline[0],streamline[14]))#rpm
			gear_rpm_speed.points_list_t[2].append((streamline[0],streamline[9]))#GPSspeed

			roll_pitch.points_list_t[0].append((streamline[0],))
			roll_pitch.points_list_t[1].append((streamline[0],-4))
			roll_pitch.points_list_t[2].append((streamline[0],-4))

			shock_travel.points_list_t[0].append((streamline[0],-32))
			shock_travel.points_list_t[1].append((streamline[0],-32))
			shock_travel.points_list_t[2].append((streamline[0],-32))
			shock_travel.points_list_t[3].append((streamline[0],-32))

			accel_x.points_list_m[0].append((streamline[3],streamline[10]))
			accel_y.points_list_m[0].append((streamline[3],streamline[11]))
			brake_tps_steering.points_list_m[0].append((streamline[3],(streamline[41]-streamline[40])/2))
			brake_tps_steering.points_list_m[1].append((streamline[3],streamline[16]))
			brake_tps_steering.points_list_m[2].append((streamline[3],streamline[63]))

			gear_rpm_speed.points_list_m[0].append((streamline[3],streamline[15]))
			gear_rpm_speed.points_list_m[1].append((streamline[3],streamline[14]))
			gear_rpm_speed.points_list_m[2].append((streamline[3],streamline[9]))

			roll_pitch.points_list_m[0].append((streamline[3],streamline[23]))
			roll_pitch.points_list_m[1].append((streamline[3],streamline[23]))
			roll_pitch.points_list_m[2].append((streamline[3],streamline[23]))

			shock_travel.points_list_m[0].append((streamline[3],streamline[23]))
			shock_travel.points_list_m[1].append((streamline[3],streamline[23]))
			shock_travel.points_list_m[2].append((streamline[3],streamline[23]))
			shock_travel.points_list_m[3].append((streamline[3],streamline[23]))

			accel_x.change = accel_y.change = brake_tps_steering.change = gear_rpm_speed.change = roll_pitch.change = shock_travel.change = True
			self.i+=0.016
			global j
			j+=0.5
			track_map.raw_coords=temp[int(j)%len(temp)]
			##create each sector
			sector1.currenttime = timesectors(streamline[5],1)
			#sector1.lap = int(self.i)
			sector2.currenttime = timesectors(streamline[5],2)
			#sector2.lap = int (self.i)
			sector3.currenttime = timesectors(streamline[5],3)
			#sector3.lap = int(self.i)
			progress1.progresslvl = streamline[14]  #(1+math.sin(4*math.pi*self.i))*5
			# utclbl1.utctime = accel_x.points_list_t
			# utclbl1.utcdate = accel_y.points_list_t
			gearlbl.currentgear = streamline[15]
			speedlbl.currentspeed = streamline[9]
			# frontleft.temptsur = self.i
			tpsgauge.tpsvalue = streamline[16]
			brakegauge.brakevalue = (streamline[41]-streamline[40])/2
			testtemp.temps = [streamline[47],streamline[48],streamline[49],streamline[50],streamline[51],streamline[52],streamline[53],streamline[54],streamline[55],streamline[56],streamline[57],streamline[58],streamline[59],streamline[60],streamline[61],streamline[62]]
			gg_diagram.value = [streamline[1],streamline[2]]
			bbprogress.bbvalue = streamline[42]
			coolantsector.sectorvalue = streamline[13]
			oilprsector.sectorvalue = streamline[20]
			batterysector.sectorvalue = streamline[21]
			errorsector.sectorvalue = errorfunc(streamline[17])

		##### creates the error message #
		### errorslistc has the errors #
		##### argument error is 11 bits #
		### each one represents an error from the errorslist #
		##### errors may be more than one #
		### errors return through errormessage #
		def errorfunc(self,error):
			errorslist = [11]
			errormessage = [11]
			for i,x in enumerate(error):
				if self.error[i] == '1':
					errormessage.append(self.errorslist[i])
			return errormessage

		def roll_pitch(self,*args):
			pass

		##### sectors made like shit #
		####laptime splitting in sectors #
		##### sector must pass in the function as a str #
		####is called whenever getdata() is called :( #
		def timesectors(self,laptime,sector):
			if self.sector == '1':
				lapt1 = self.laptime
				return lapt1
			if self.sector == '2':
				lapt2 = self.laptime-lapt1
				return lapt2
			if self.sector == '3':
				lapt3 = self.laptime-(lapt2+lapt1)
				return lapt3


	try:
		TelemetryApp().run()
	except Exception as e:
		# ser.close()

		raise e

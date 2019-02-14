#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial,time,kivy,math,random,queue
kivy.require('1.10.0')
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
import itertools
from kivy.uix.widget import Widget
from screen1 import *
if __name__ == '__main__':
	i = 0
	class Telemetry_App(App):
		changing = ScreenManager()
		def build(self):
			box= FloatLayout()
			Window.clearcolor = (85/256,23/256,23/256,1)
			for i in range(4):
				screen = Screen(name= 'Title %d' % i)
				self.changing.add_widget(screen)

				main=FloatLayout()
				screen.add_widget(main)

				main.add_widget(
					Label(
						text= 'I am screen No%d' % i,
						font_size= '40sp',
						pos_hint= {'x':0.4,'y':0.4},
            			size_hint= (0.2,0.2)
					)
				)
				main.add_widget(
					Image(
					source= "Images/prom.png",
					pos_hint= {'x':0.1,'y':0.5},
					size_hint= (0.8,0.2)
					)
				)
			box.add_widget(self.changing)
			box.add_widget(imported_widget)
			box.add_widget(
					Image(
					source= "Images/NTUA.png",
					pos_hint= {'x':0.1,'y':0.8},
					size_hint= (0.8,0.2)
					)
				)

			Clock.schedule_interval(lambda *t: self.letsgo(), 1)
			return box
		def letsgo(self):
			global i
			i+=1
			self.changing.current = 'Title %d'% (i%4)
	try:
		Telemetry_App().run()
	except Exception as e:
		raise e

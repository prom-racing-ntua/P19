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
if __name__ == '__main__':
	i = 0
	class Telemetry_App(App):
		sm = ScreenManager()
		def build(self):
			box = GridLayout(cols=3)
			Window.clearcolor = (23/256,23/256,23/256,1)
			col1 = FloatLayout()
			self.c = Label(text= "Hello World")
			box.add_widget(self.c)
			for i in range(4):
				screen = Screen(name= 'Title %d' % i)
				screen.add_widget(Label(text= 'Hello World %d' % i))
				self.sm.add_widget(screen)

			Clock.schedule_interval(lambda *t: self.letsgo(), 1)
			return self.sm
		def letsgo(self):
			global i
			i+=1
			self.sm.current = 'Title %d'% (i%4)
	try:
		Telemetry_App().run()
	except Exception as e:
		raise e

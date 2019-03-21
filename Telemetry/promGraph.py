from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from customGraph import Graph
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.garden.graph import LinePlot, MeshLinePlot
from hover import HoverBehavior
from collections import deque
from customLabel import CustomLabel
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner

margin = [1,5,7,10]
RGB = [[1, 0, 0, 1],[0, 1, 0, 1],[0, 0, 1, 1],[1, 0, 1, 1],[0, 1, 1, 1]]

class PromGraph(Graph,Widget,HoverBehavior):
	num_of_plots = NumericProperty()
	change = BooleanProperty(False)
	by_meters = BooleanProperty(False)
	by_time = BooleanProperty(False)
	size_text = StringProperty('17sp')
	points_list_m = ListProperty([])
	points_list_t = ListProperty([])
	diagrams = ListProperty([])
	labs = ListProperty([])
	ylabs = ListProperty([])
	marg = NumericProperty(margin[0])

	def __init__(self, **kwargs):
		super(PromGraph, self).__init__(**kwargs)
		for i in range(self.num_of_plots):
			self.points_list_m.append(deque(maxlen=1250))
			self.points_list_t.append(deque(maxlen=1250))
			self.diagrams.append(LinePlot(line_width=2, color=RGB[i]))
			self.add_plot(self.diagrams[i])
			self.labs.append(CustomLabel(text ='', font_size=self.size_text, color=RGB[i], bgclr=RGB[i]))
			self.add_widget(self.labs[i])
		self.switch_t = CheckBox(group=str(self),size=(30,30))
		self.switch_m = CheckBox(group=str(self),size=(30,30))
		self.switch_t.bind(active=self._is_switched_t)
		self.switch_m.bind(active=self._is_switched_m)
		self.spinner = Spinner(
			text='%s sec' % margin[0],
	    	values=('%s sec'% margin[0],'%s sec'% margin[1],'%s sec'% margin[2],'%s sec'% margin[3]),
	    	size=(50,20))
		self.add_widget(self.spinner)
		self.add_widget(self.switch_t)
		self.add_widget(self.switch_m)
		self.bind(change = self.update)
		self.bind(pos = self.shape)
		self.bind(size = self.shape)
		self.spinner.bind(text = self.show_selected_value)

	def update(self,*args):
		if self.by_meters:
			for i in range(self.num_of_plots):
				self.diagrams[i].points = self.points_list_m[i]
				self.labs[i].text = self.ylabs[i]%self.points_list_m[i][-1][1]
		elif self.by_time:
			for i in range(self.num_of_plots):
				self.diagrams[i].points = self.points_list_t[i]
				self.labs[i].text = self.ylabs[i]%self.points_list_t[i][-1][1]
		else:
			for i in range(self.num_of_plots):
				self.diagrams[i].points = []
				self.labs[i].text = ""
		self.xmin = self.points_list_t[0][-1][0]-self.marg
		self.xmax = self.points_list_t[0][-1][0]
		self.change = False

	def shape(self,*args):
		w=self.width/self.num_of_plots
		self.switch_t.center = self.right,self.top-80
		self.switch_m.center = self.right,self.top-110
		self.spinner.center = self.right-40,self.top-20

		for i in range(self.num_of_plots):
			self.labs[i].center = (self.x+(i*0.8+0.7)*w,self.top-self.height/5)
	def _is_switched_m(self,checkbox, value):
		self.by_meters=not(self.by_meters)
	def _is_switched_t(self,checkbox, value):
		self.by_time=not(self.by_time)
	def show_selected_value(self,spinner, text):
		self.marg = int(text.split()[0])
		self.x_ticks_major = int(text.split()[0])/5



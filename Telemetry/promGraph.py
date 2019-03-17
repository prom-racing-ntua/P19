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

RGB=[[1, 0, 0, 1],[0, 1, 0, 1],[0, 0, 1, 1],[1, 0, 1, 1],[0, 1, 1, 1]]

class PromGraph(Graph,Widget,HoverBehavior):
	num_of_plots = NumericProperty()
	change = BooleanProperty(False)
	by_meters = BooleanProperty(False)
	size_text = StringProperty('17sp')
	points_list_m = ListProperty([])
	points_list_t = ListProperty([])
	diagrams = ListProperty([])
	labs = ListProperty([])
	ylabs=ListProperty([])

	def __init__(self, **kwargs):
		super(PromGraph, self).__init__(**kwargs)
		for i in range(self.num_of_plots):
			self.points_list_m.append(deque(maxlen=300))
			self.points_list_t.append(deque(maxlen=300))
			self.diagrams.append(LinePlot(line_width=2, color=RGB[i]))
			self.add_plot(self.diagrams[i])
			self.labs.append(CustomLabel(text ='', font_size=self.size_text,color=RGB[i],bgclr=RGB[i]))
			self.add_widget(self.labs[i])
			print(self.children)
		self.bind(change = self.update)
		self.bind(pos = self.shape)
		self.bind(size = self.shape)

	def update(self,*args):
		if self.by_meters:
			for i in range(self.num_of_plots):
				self.diagrams[i].points = self.points_list_m[i]
				self.labs[i].text = self.ylabs[i]%self.points_list_m[i][-1][1]

		else:
			for i in range(self.num_of_plots):
				self.diagrams[i].points = self.points_list_t[i]
				self.labs[i].text = self.ylabs[i]%self.points_list_t[i][-1][1]
		self.change=False
	def shape(self,*args):
		w=self.width/self.num_of_plots
		for i in range(self.num_of_plots):
			self.labs[i].center = (self.x+(i*0.8+0.7)*w,self.top-self.height/5)

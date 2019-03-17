from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout

from customGraph import Graph
from kivy.garden.graph import LinePlot, MeshLinePlot
from promGraph import PromGraph


left_column = FloatLayout()
roll_pitch = PromGraph(
				ylabs=["ROLLF: %.2f","ROLLR: %.2f","PITCH: %.2f"],
				num_of_plots=3,
				xlabel='',
				ylabel='',
				precisionx='%.2f',
				x_ticks_minor=2,
				x_ticks_major=1,
				y_ticks_major=1,
				y_grid_label=True,
				x_grid_label=True,
				padding=5,
				xlog=False,
				ylog=False,
				x_grid=True,
				y_grid=True,
				ymin=-5,
				ymax=5,
				pos_hint={'x':0,'y':0.25},
				size_hint=(0.3,0.3)
				)
left_column.add_widget(roll_pitch)

shock_travel = PromGraph(
				ylabs=["FL: %.2f","FR: %.2f","RL: %.2f","RR: %.2f"],
				num_of_plots=4,
				xlabel='',
				ylabel='',
				precisionx='%.2f',
				size_text='13sp',
				x_ticks_minor=2,
				x_ticks_major=1,
				y_ticks_major=20,
				y_grid_label=True,
				x_grid_label=True,
				padding=5,
				xlog=False,
				ylog=False,
				x_grid=True,
				y_grid=True,
				ymin=0,
				ymax=100,
				pos_hint={'x':0,'y':0.55},
				size_hint=(0.3,0.3)
				)
left_column.add_widget(shock_travel)

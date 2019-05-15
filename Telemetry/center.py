from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from customGraph import Graph
from kivy.garden.graph import LinePlot, MeshLinePlot
from promGraph import PromGraph
from datetime import *
from sectors import Sectors
#from utcLabel import UtcLabel
from utclbl import UtcLbl
from tempsectors import TempSectors


center_column = FloatLayout()
accel_x = PromGraph(
				ylabs=["AX: %.2f"],
				num_of_plots=1,
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
				ymin=-3,
				ymax=3,
				pos_hint={'x':0.3,'y':0},
				size_hint=(0.4,0.23)
				)
center_column.add_widget(accel_x)

accel_y = PromGraph(
				ylabs=["AY: %.2f"],
				num_of_plots=1,
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
				ymin=-3,
				ymax=3,
				pos_hint={'x':0.3,'y':0.21},
				size_hint=(0.4,0.23)
				)
center_column.add_widget(accel_y)

gear_rpm_speed = PromGraph(
				ylabs=["GEAR: %.2f","RPM: %.2f","SPD: %.2f"],
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
				ymin=0,
				ymax=5,
				ymin1=0,
				ymax1=10000,
				ymin2=0,
				ymax2=120,
				pos_hint={'x':0.3,'y':0.42},
				size_hint=(0.4,0.23)
				)
center_column.add_widget(gear_rpm_speed)

brake_tps_steering = PromGraph(
				ylabs=["BRAKE: %.2f","TPS: %.2f","STEER: %.2f"],
				num_of_plots=3,
				xlabel='',
				ylabel='',
				precisionx='%.2f',
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
				pos_hint={'x':0.3,'y':0.63},
				size_hint=(0.4,0.23)
				)
center_column.add_widget(brake_tps_steering)


center_column.add_widget(Image(
			source="Images/prom_logo.png",
			pos_hint={'x':0.40,'y':0.82},
			size_hint=(0.20,0.20)))




# utclbl1 = UtcLbl (
# 	pos_hint = {'x':0.5,'y':0.85},
#     size_hint = (0.09,0.15)
# 	)
# utclbl1.lineclr = [1,1,1,0]
# utclbl1.timelabel.lineclr = [1,1,1,0]
# utclbl1.datelabel.lineclr=[1,1,1,0]
# center_column.add_widget(utclbl1)

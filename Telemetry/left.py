from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout

from customGraph import Graph
from kivy.garden.graph import LinePlot, MeshLinePlot
from promGraph import PromGraph
from trackmap import TrackMap
from tiretemp import TiretempLbl
from customcolor import *
from tempsectors import TempSectors


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
				ymin=-1.5,
				ymax=1.5,
				pos_hint={'x':0,'y':0},
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
				ymin=-30,
				ymax=30,
				pos_hint={'x':0,'y':0.30},
				size_hint=(0.3,0.3)
				)
left_column.add_widget(shock_travel)

track_map = TrackMap()
wrapper_relative=RelativeLayout(pos_hint={'x':0.8,'y':0.3},
				size_hint=(0.2,0.2))
wrapper_relative.add_widget(track_map)
left_column.add_widget(wrapper_relative)

# frontleft = TiretempLbl (
#     pos_hint = {'x':0.01,'y':0.89},
#     size_hint = (0.05,0.1)
# 	)
# # left_column.add_widget(frontleft)
# frontright = TiretempLbl (
# 	pos_hint = {'x':0.07,'y':0.89},
# 	size_hint = (0.05,0.1)
# )
# # left_column.add_widget(frontright)
# frontright.templbl.text = 'fr'
# backleft = TiretempLbl (
#     pos_hint = {'x':0.01,'y':0.79},
#     size_hint = (0.05,0.1)
# 	)
# # left_column.add_widget(backleft)
# backright = TiretempLbl (
#     pos_hint = {'x':0.07,'y':0.79},
#     size_hint = (0.05,0.1)
# 	)
# left_column.add_widget(backright)

####### TEMP SECTORS #########

coolantsector = TempSectors(
	sectorname = 'Coolant',
	sectorvalue = '97oC',
	pos_hint = {'x':0., 'y':0.96},
	size_hint = (0.08,0.04)
)
left_column.add_widget(coolantsector)
oilprsector = TempSectors(
	sectorname = 'Oil Pressure',
	sectorvalue = '3 bar',
	pos_hint = {'x':0.,'y':0.92},
	size_hint = (0.08,0.04)
)
left_column.add_widget(oilprsector)

oiltempsector = TempSectors(
	sectorname = 'Oil Temp',
	sectorvalue = '137oC',
	pos_hint = {'x':0.,'y':0.88},
	size_hint = (0.08,0.04)
)
left_column.add_widget(oiltempsector)

afrsector = TempSectors (
	sectorname = 'AFR',
	sectorvalue = '13.2',
	pos_hint = {'x':0.16,'y':0.96},
	size_hint = (0.08,0.04)
)
left_column.add_widget(afrsector)

batterysector = TempSectors (
	sectorname = 'Battery',
	sectorvalue = '13.2 V',
	pos_hint = {'x':0.16,'y':0.92},
	size_hint = (0.08,0.04)

)
left_column.add_widget(batterysector)

errorsector = TempSectors (
	sectorname = 'ERROR',
	sectorvalue = '-',
	pos_hint = {'x':0.16,'y':0.88},
	size_hint = (0.08,0.04)
)
left_column.add_widget(errorsector)

######### TIRE TEMP #################
testtemp = TiretempLbl(
	pos_hint={'x':0.01,'y':0.62},
	size_hint = (0.13,0.20)
)
left_column.add_widget(testtemp)

from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout

from customGraph import Graph
from kivy.garden.graph import LinePlot, MeshLinePlot
from promGraph import PromGraph
from sectors import *


right_column = FloatLayout()

sector1 = Sectors(
	sectorname = "Sector 1",
	customcolor = [0.35,0.35,0.35,1],
	pos_hint = {'x':0.7,'y':0.85},
	size_hint = (0.1,0.15)

)
right_column.add_widget(sector1)

sector2 = Sectors (
    sectorname = "Sector 2",
    customcolor = [0.55,0.35,0.35,1],
    pos_hint = {'x':0.8,'y':0.85},
    size_hint=(0.1,0.15)
)
right_column.add_widget(sector2)

sector3 = Sectors(
    sectorname = "Sector 3",
    customcolor = [0.35 , 0.55 , 0.35 , 1],
    pos_hint = {'x':0.9,'y':0.85},
    size_hint=(0.1,0.15)
)
right_column.add_widget(sector3)

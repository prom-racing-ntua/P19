from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout

from customGraph import Graph
from kivy.garden.graph import LinePlot, MeshLinePlot
from promGraph import PromGraph
from sectors import *
from progressbar import *

right_column = FloatLayout()
indication = Sectors(
    sectorname = " ",
    #customcolor = [1,1,1,0],
    pos_hint = {'x':0.62 , 'y':0.865},
    size_hint = (0.07,0.15)
)
indication.currentlabel.text = 'this'
indication.previouslabel.text = 'pr.best'
indication.bestlabel.text = 'best'
indication.sectorlabel.lineclr = [1,1,1,0]
indication.currentlabel.lineclr = [1,1,1,0]
indication.previouslabel.lineclr = [1,1,1,0]
indication.bestlabel.lineclr = [1,1,1,0]
# indication.sectorlabel.bgclr = [1,1,1,0.5]
# indication.currentlabel.bgclr = [1,1,1,0.5]
# indication.previouslabel.bgclr = [1,1,1,0.5]
# indication.bestlabel.bgclr = [1,1,1,0.5]

right_column.add_widget(indication)

laps = Sectors(
   sectorname = "Lap",
   pos_hint = {'x':0.69,'y':0.865},
   size_hint = (0.04,0.15)
)
right_column.add_widget(laps)

sector1 = Sectors(
	sectorname = "Sector 1",
	customcolor = [0.35,0.35,0.35,1],
	pos_hint = {'x':0.73,'y':0.865},
	size_hint = (0.09,0.15)

)
right_column.add_widget(sector1)

sector2 = Sectors (
    sectorname = "Sector 2",
    customcolor = [0.55,0.35,0.35,1],
    pos_hint = {'x':0.82,'y':0.865},
    size_hint=(0.09,0.15)
)
right_column.add_widget(sector2)

sector3 = Sectors(
    sectorname = "Sector 3",
    customcolor = [0.35 , 0.55 , 0.35 , 1],
    pos_hint = {'x':0.91,'y':0.865},
    size_hint=(0.09,0.15)
)
right_column.add_widget(sector3)

progress1 = ProgressBa(
	lowclr1 = [0.2,0,1,1],
    lowclr2 = [0.5,0,1,1],
    lowclr3 = [0.8,0,1,1],
    med1clr1 = [1,1,1,1],
    med1clr2 = [1,1,1,1],
    med1clr3 = [1,1,1,1],
    med2clr1 = [1,1,1,1],
    med2clr2 = [1,1,1,1],
    med2clr3 = [1,1,1,1],
    highclr1 = [1,1,1,1],
    highclr2 = [1,1,1,1],
    highclr3 = [1,1,1,1],
    anglestart =-90,
    anglestop =0,
	pos_hint = {'x':0.7,'y':0.3},
    size_hint=(0.4,0.3))
right_column.add_widget(progress1)

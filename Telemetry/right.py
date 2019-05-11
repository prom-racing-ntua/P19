from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout

from customGraph import Graph
from kivy.garden.graph import LinePlot, MeshLinePlot
from promGraph import PromGraph
from sectors import *
from progressbar import ProgressBa
from progressbar2 import ProgressBar2
from gearlbl import GearLabel
from speedlbl import SpeedLabel
from warning_Label import WarningLabel
from gaugeprbar import TPSGauge
from brakegauge import BrakeGauge

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

progress1 = ProgressBa (
    lowclr1 = [1,1,0,0.5],
    lowclr2 = [1,1,0,0.6],
    lowclr3 = [1,1,0,0.7],
    lowclr4 = [1,1,0,0.8],
    lowclr5 = [1,1,0,0.9],
    lowclr6 = [1,1,0,1],
    med1clr1 = [0.6,1,0.2,1],
    med1clr2 = [0.5,1,0.3,1],
    med1clr3 = [0.4,1,0.4,1],
    med1clr4 = [0.3,1,0.3,1],
    med1clr5 = [0.2,1,0.2,1],
    med1clr6 = [0.1,1,0.1,1],
    # med1clr7 = [0,1,0,1],
    # med1clr8 = [0,1,0,1],
    # med1clr9 = [0,1,0,1],
    # med1clr10 = [0,1,0,1],
    # med1clr11 = [0,1,0,1],
    # med1clr12 = [0,1,0,1],
    med2clr1 = [0,1,0.8,1],
    med2clr2 = [0,0.75,1,1],
    med2clr3 = [0,0.7,1,1],
    med2clr4 = [0,0.65,1,1],
    med2clr5 = [0,0.75,1,1],
    med2clr6 = [0,0.65,1,1],
    med2clr7 = [0,0.55,1,1],
    med2clr8 = [0,0.45,1,1],
    med2clr9 = [0,0.35,1,1],
    med2clr10 = [0,0.25,1,1],
    med2clr11 = [0,0.15,1,1],
    med2clr12 = [0,0,1,1],
    highclr1 = [1,0,0,1],
    highclr2 = [1,0,0,0.9],
    highclr3 = [1,0,0,1],
    anglestart = 270,
    anglestop = 390,
    pos_hint = {'x':0.72 , 'y':0.38},
    size_hint = (0.41,0.2)
)
right_column.add_widget(progress1)



# progresstest = ProgressBar2 (
#     anglestart = 270,
#     anglestop = 390,
#     pos_hint = {'x':0.72 , 'y':0.18},
#     size_hint = (0.41,0.2)
# )
#right_column.add_widget(progresstest)

gearlbl = GearLabel (
    currentgear = 0,
	customcolor = [0.35,0.35,0.35,1],
	pos_hint = {'x':0.82,'y':0.72},
	size_hint = (0.1,0.10),
)
right_column.add_widget(gearlbl)

speedlbl = SpeedLabel (
    currentspeed = 0,
    pos_hint = {'x': 0.76, 'y':0.70},
    size_hint = (0.09 , 0.10)
)
right_column.add_widget (speedlbl)

warning1 = WarningLabel (
    name = "Sensor1",
    pos_hint = {'x':0.50,'y':0.50},
    size_hint = (0.09,0.10)
)
right_column.add_widget(warning1)

warning2 = WarningLabel (
    name = "Sensor2",
    pos_hint = {'x':0.50,'y':0.50},
    size_hint = (0.09,0.10)
)
right_column.add_widget(warning2)

warning3 = WarningLabel (
    name = "Sensor3",
    pos_hint = {'x':0.50,'y':0.50},
    size_hint = (0.09,0.10)
)
right_column.add_widget(warning3)

warning4 = WarningLabel (
    name = "Sensor4",
    pos_hint = {'x':0.50,'y':0.50},
    size_hint = (0.09,0.10)
)
right_column.add_widget(warning4)

warning5 = WarningLabel (
    name = "Sensor5",
    pos_hint = {'x':0.50,'y':0.50},
    size_hint = (0.09,0.10)
)
right_column.add_widget(warning5)

warning6 = WarningLabel (
    name = "Sensor6",
    pos_hint = {'x':0.50,'y':0.50},
    size_hint = (0.09,0.10)
)
right_column.add_widget(warning6)

tpsgauge = TPSGauge (
    pos_hint = {'x':0.76,'y':0.6},
    size_hint = (0.2,0.1)
)
right_column.add_widget(tpsgauge)

brakegauge = BrakeGauge (
    pos_hint = {'x':0.76,'y':0.6},
    size_hint = (0.2,0.1)
)
# right_column.add_widget(brakegauge)

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
from brakebiaspb import BrakeBiasPB
from tempsectors import TempSectors
from accel import Accel

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
    med2clr1 = [0.1,1,0.34,1],
    med2clr2 = [0.1,1,0.51,1],
    med2clr3 = [0.1,1,0.69,1],
    med2clr4 = [0.1,1,0.9,1],
    med2clr5 = [0.1,0.94,1,1],
    med2clr6 = [0.1,0.7,1,1],
    med2clr7 = [0.1,0.51,1,1],
    med2clr8 = [0.1,0.38,1,1],
    med2clr9 = [0.1,0.27,1,1],
    med2clr10 = [0.1,0.1,1,1],
    med2clr11 = [0.27,0.1,1,1],
    med2clr12 = [0.58,0.1,1,1],
    highclr1 = [1,0.19,0,1],
    highclr2 = [1,0.10,0,1],
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

tpsgauge = TPSGauge (
    pos_hint = {'x':0.89,'y':0.63},
    size_hint = (0.1,0.1)
)
right_column.add_widget(tpsgauge)

brakegauge = BrakeGauge (
    pos_hint = {'x':0.86,'y':0.63},
    size_hint = (0.1,0.1)
)
right_column.add_widget(brakegauge)

bbprogress = BrakeBiasPB(
    pos_hint = {'x':0.77,'y':0.59},
    size_hint = (0.1,0.00001)
)
right_column.add_widget(bbprogress)

###### TEMP SECTORS #########

dfsector = TempSectors(
	sectorname = 'Downforce',
	sectorvalue = '97kg',
	pos_hint = {'x':0.7, 'y':0.20},
	size_hint = (0.07,0.04)
)
right_column.add_widget(dfsector)
gripsector = TempSectors(
	sectorname = 'Grip',
	sectorvalue = '100',
	pos_hint = {'x':0.7,'y':0.16},
	size_hint = (0.07,0.04)
)
right_column.add_widget(gripsector)

understeersector = TempSectors(
	sectorname = 'Understeer',
	sectorvalue = '00000',
	pos_hint = {'x':0.7,'y':0.12},
	size_hint = (0.07,0.04)
)
right_column.add_widget(understeersector)

yawgsector = TempSectors (
	sectorname = 'Yaw g',
	sectorvalue = '00000',
	pos_hint = {'x':0.7,'y':0.08},
	size_hint = (0.07,0.04)
)
right_column.add_widget(yawgsector)

lockupsector = TempSectors (
	sectorname = 'Lock up',
	sectorvalue = 'fl',
	pos_hint = {'x':0.7,'y':0.04},
	size_hint = (0.07,0.04)
)
right_column.add_widget(lockupsector)

slipratiosector = TempSectors (
	sectorname = 'Slip Ratio',
	sectorvalue = '123:45',
	pos_hint = {'x':0.7,'y':0.},
	size_hint = (0.07,0.04)
)
right_column.add_widget(slipratiosector)

gg_diagram = Accel(
    value=[0,0],
    size_backgnd=220,
    size_text=20,
    widget_unit='g',
    widget_name="Acceleration",
    pos_hint = {'x':0.84,'y':0.02},
    size_hint = (0.15,0.24)
    )
right_column.add_widget(gg_diagram)

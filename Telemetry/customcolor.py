import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty,StringProperty, ListProperty
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from sectorLabel import SectorLabel

class CustomColor ():
    def __init__(self,**kwargs):
        rgbfile = open('rgbvalues.txt') # Open file on read mode
        lines = rgbfile.read().split("\n") # Create a list containing all lines
        customcolor = lines
        print (customcolor)
        rgbfile.close() # Close file
        return customcolor

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty,StringProperty, ListProperty,BoundedNumericProperty
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from sectorLabel import SectorLabel


class ProgressRect (Widget):
  

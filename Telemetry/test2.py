##--test2widget--##
import kivy
kivy.require('1.10.0')
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from kivy.uix.image import Image
from hover import HoverBehavior

from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty,ListProperty


Builder.load_string('''
<Test2Widget>
    id : original
    canvas:
        Color:
            rgba: [0,1,0,1] if self.hovered else [0,0,1,1]








''')

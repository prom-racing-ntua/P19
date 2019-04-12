import kivy
kivy.require('1.10.0')
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from kivy.uix.image import Image
from hover import HoverBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty,ListProperty
from kivy.uix.relativelayout import RelativeLayout


Builder.load_string('''
<Warning_Table>:
    Label:
        text: str
        font_size: '10sp'



''')
class Warning_Table(Widget,HoverBehavior):
    lbltext = StringProperty('')
    numoflabels = NumericProperty()

    def __init__(self, **kwargs):
        super(Warning_Table, self).__init__(**kwargs)

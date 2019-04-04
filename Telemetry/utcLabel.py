# utcdatetime.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
from kivy.lang import Builder
from kivy.uix.image import Image
from hover import HoverBehavior
from sectors import Sectors

from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty,ListProperty

class UtcLabel (Sectors , Widget):
    # lineclr = ListProperty([])
    # bgclr = ListProperty([])
    utctime = ListProperty([])
    utcdate = ListProperty([])
    def __init__(self,utctime=None,utcdate=None,**kwargs):
        self.utctime = utctime if utctime is not None  else datetime.time()
        self.utcdate = utcdate if utcdate is not None else datetime.date()
        super(UtcLabel, self).__init__(**kwargs)
        self.bind(utctime = _changedatetime )
        self.bind(utcdate = _changedatetime )
        def _changedatetime(self, *args):
            self.currentlabel.text = str(datetime.utcnow())

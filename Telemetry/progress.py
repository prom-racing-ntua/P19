# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.properties import ListProperty, OptionProperty, BooleanProperty,NumericProperty
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
from kivymd.theming import ThemableBehavior
from kivy.uix.progressbar import ProgressBar
from kivymd.theming import ThemeManager
from kivy.graphics import Color


Builder.load_string('''
<MDProgressBar>:
    canvas:
        Clear
        Color:
            rgba:  self.color1
        Rectangle:
            size:    (self.width , dp(4)*3) if self.orientation == 'horizontal' else (dp(4)*self.sizex,self.height/self.sizey)
            pos:   (self.x, self.center_y - dp(4)) if self.orientation == 'horizontal' \
                else (self.center_x - dp(4),self.y)


        Color:
            rgba:  self.color2
        Rectangle:
            size:     (self.width*self.value_normalized, sp(4)*3) if self.orientation == 'horizontal' else (sp(4)*self.sizex, \
                self.height*self.value_normalized/self.sizey)
            pos:    (self.width*(1-self.value_normalized)+self.x if self.reversed else self.x, self.center_y - dp(4)) \
                if self.orientation == 'horizontal' else \
                (self.center_x - dp(4),self.height*(1-self.value_normalized)+self.y if self.reversed else self.y)

''')


class MDProgressBar(ThemableBehavior, ProgressBar):
    reversed = BooleanProperty(False)
    ''' Reverse the direction the progressbar moves. '''
    theme_cls = ThemeManager()
    color1=ListProperty(theme_cls.divider_color)
    color2=ListProperty(theme_cls.primary_color)
    sizex=NumericProperty(8)
    sizey=NumericProperty(1)
    # color1=theme_cls.divider_color
    # color2=theme_cls.primary_color
    orientation = OptionProperty('horizontal', options=['horizontal', 'vertical'])
    ''' Orientation of progressbar'''


# if __name__ == '__main__':
#     from kivy.app import App
#     from kivymd.theming import ThemeManager

#     class ProgressBarApp(App):
#         theme_cls = ThemeManager()

#         def build(self):
#             return Builder.load_string("""#:import MDSlider kivymd.slider.MDSlider
# BoxLayout:
#     orientation:'vertical'
#     padding: '8dp'
#     MDSlider:
#         id:slider
#         min:0
#         max:100
#         value: 40

#     MDProgressBar:
#         value: slider.value
#     MDProgressBar:
#         reversed: True
#         value: slider.value
#     BoxLayout:
#         MDProgressBar:
#             orientation:"vertical"
#             reversed: True
#             value: slider.value

#         MDProgressBar:
#             orientation:"vertical"
#             value: slider.value

# """)


#     ProgressBarApp().run()

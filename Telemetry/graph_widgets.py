from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from customGraph import Graph
from kivy.garden.graph import LinePlot, MeshLinePlot



main_window = FloatLayout()
accel_x = Graph(
				xlabel='',
				ylabel='',
				precisionx='%.2f',
				x_ticks_minor=2,
				x_ticks_major=1,
				y_ticks_major=1,
				y_grid_label=True,
				x_grid_label=True,
				padding=5,
				xlog=False,
				ylog=False,
				x_grid=True,
				y_grid=True,
				ymin=-3,
				ymax=3,
				pos_hint={'x':0.3,'y':0},
				size_hint=(0.4,0.23)
				)
main_window.add_widget(accel_x)

accel_y = Graph(
				xlabel='',
				ylabel='',
				precisionx='%.2f',
				x_ticks_minor=2,
				x_ticks_major=1,
				y_ticks_major=1,
				y_grid_label=True,
				x_grid_label=True,
				padding=5,
				xlog=False,
				ylog=False,
				x_grid=True,
				y_grid=True,
				ymin=-3,
				ymax=3,
				pos_hint={'x':0.3,'y':0.21},
				size_hint=(0.4,0.23)
				)
main_window.add_widget(accel_y)

gear_rpm_speed = Graph(
				xlabel='',
				ylabel='',
				ylabel1='RPM',
				ylabel2='SPEED',
				precisionx='%.2f',
				x_ticks_minor=2,
				x_ticks_major=1,
				y_ticks_major=1,
				y_grid_label=True,
				x_grid_label=True,
				padding=5,
				xlog=False,
				ylog=False,
				x_grid=True,
				y_grid=True,
				ymin=0,
				ymax=5,
				ymin1=0,
				ymax1=10000,
				ymin2=0,
				ymax2=120,
				pos_hint={'x':0.3,'y':0.42},
				size_hint=(0.4,0.23)
				)
main_window.add_widget(gear_rpm_speed)

brake_tps_steering = Graph(
				xlabel='',
				ylabel='',
				ylabel1='RPM',
				ylabel2='SPEED',
				precisionx='%.2f',
				x_ticks_minor=2,
				x_ticks_major=1,
				y_ticks_major=20,
				y_grid_label=True,
				x_grid_label=True,
				padding=5,
				xlog=False,
				ylog=False,
				x_grid=True,
				y_grid=True,
				ymin=0,
				ymax=100,
				pos_hint={'x':0.3,'y':0.63},
				size_hint=(0.4,0.23)
				)
main_window.add_widget(brake_tps_steering)


ax_plot = LinePlot(line_width=2, color=[1, 0, 0, 1])
ay_plot = LinePlot(line_width=2, color=[1, 0, 0, 1])
gear_plot = LinePlot(line_width=2, color=[0, 0, 1, 1])
rpm_plot = LinePlot(line_width=2, color=[0, 0, 1, 1])
speed_plot = LinePlot(line_width=2, color=[0, 0, 1, 1])
tps_plot = LinePlot(line_width=2, color=[0, 0, 1, 1])
brake_plot = LinePlot(line_width=2, color=[0, 0, 1, 1])
steering_plot = LinePlot(line_width=2, color=[0, 0, 1, 1])


accel_x.add_plot(ax_plot)
accel_y.add_plot(ay_plot)
gear_rpm_speed.add_plot(speed_plot)
gear_rpm_speed.add_plot(rpm_plot)
gear_rpm_speed.add_plot(gear_plot)
brake_tps_steering.add_plot(brake_plot)
brake_tps_steering.add_plot(tps_plot)
brake_tps_steering.add_plot(steering_plot)



brake_tps_steering.xmax = gear_rpm_speed.xmax = accel_x.xmax = accel_y.xmax = 5
brake_tps_steering.xmin = gear_rpm_speed.xmin = accel_x.xmin = accel_y.xmin = 0


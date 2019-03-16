using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using LiveCharts;
using LiveCharts.Wpf;
using System.Windows.Media;


namespace winformsbase
{
    public partial class Form1 : Form
    {
        //prtivate List<double> valueslist = new List<double>();
        public Form1()
        {
            InitializeComponent();

            cartesianChart1.Series.Add(new LineSeries
            {
                Values = new ChartValues<double> { 1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 1, 2, 3, 5, 4, 3, 2, 1, 5, 6, 7 },
                ScalesYAt = 0
            });
            cartesianChart1.Series.Add(new LineSeries
            {
                Values = new ChartValues<double> { 11, 2, 21, 3, 6, 5, 6, 1, 1, 19, 11, 12, 13, 4, 5, 1, 2, 3, 15, 20, 13, 2, 11, 5, 6, 7 },
                ScalesYAt = 1
            });
            cartesianChart1.AxisY.Add(new Axis
            {
                Foreground = System.Windows.Media.Brushes.DodgerBlue,
                Title = "Blue Axis"
            });
            cartesianChart1.AxisY.Add(new Axis
            {
                Foreground = System.Windows.Media.Brushes.Black,
                Title = "bLACK Axis",
                Position = AxisPosition.RightTop
            });

            //SOLID GAUGES

            solidGauge1.From = 0;
            solidGauge1.To = 100;
            solidGauge1.Value = 50;
            //solidGauge1.Base.LabelsVisibility = Visibility.Hidden;
            solidGauge1.Base.GaugeActiveFill = new LinearGradientBrush
            {
                GradientStops = new GradientStopCollection
                {
                    new GradientStop(Colors.Yellow, 0),
                    new GradientStop(Colors.Orange, .5),
                    new GradientStop(Colors.Red, 1)
                }

            };
        }
    }
}

using System;
using System.IO.Ports;
using System.Windows.Forms;


namespace Serial_Connection_Test
{
    public partial class Form1 : Form
    {   private String mStr;
        private String port;
        public Form1()
        {
            InitializeComponent();
        }

 

        private void Form1_Load(object sender, EventArgs e)
        {  
            foreach (string ports in SerialPort.GetPortNames())
            {
                comboBox1.Items.Add(ports);
                comboBox1.Text = ports;
            }
            textBox2.ScrollBars = ScrollBars.Vertical;

        }

 
        private void button1_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                serialPort1.WriteLine(textBox1.Text);
            }
            Console.WriteLine(textBox1.Text);
            textBox1.Text ="";

        }

        private void button2_Click(object sender, EventArgs e)
        {
            serialPort1.BaudRate = 9600;
            serialPort1.PortName = port;
            if (!serialPort1.IsOpen) {
                serialPort1.Open();
            }

        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            port = comboBox1.SelectedItem.ToString();
        }

        private void serialPort1_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            mStr = serialPort1.ReadLine();
            textBox2.Text= textBox2.Text+mStr+"\n";

        }

        ~Form1()
        {
            serialPort1.Close();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        
    }
}

using System;
using System.IO.Ports;
using System.Windows.Forms;
using System.Threading;


namespace Serial_Connection_Test
{
    public partial class Form1 : Form
    { private String mStr;
        private String port;
        private int counter;
        private String fancy = "/-\\|";
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

            serialPort1.Write(textBox1.Text);
            Console.WriteLine(textBox1.Text);
            textBox1.Text = "";

        }

        private void button2_Click(object sender, EventArgs e)
        {

            if (!serialPort1.IsOpen) {
                serialPort1.BaudRate = 9600;
                serialPort1.PortName = port;
                serialPort1.Open();
                Thread readThread = new Thread(Read);
                readThread.Start();
                timer1.Start();
            }

        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            port = comboBox1.SelectedItem.ToString();
        }


        ~Form1()
        {
            serialPort1.Close();
            timer1.Stop();
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            counter++;
            textBox2.Text = mStr;

        }
        public void Read()
        {
            while (true)
            {
                try
                {
                    mStr = serialPort1.ReadLine() + fancy[counter % 3] + "\n";
                }
                catch {
                    Console.WriteLine("TON POULO");
                }


        }
        }

    }




}
 #include <PID_v1.h>
//        (SCK)-D13   D12-(MISO)
//        3.3V  D11- (MOSI)(PWM)
//              REF   D10-(SS)(PWM)
//              A0    D9              :HALFDOWN
//              A1    D8              :HALFUP
//              A2    D7              :DOWN
//              A3    D6-(PWM)        :M2/N2
//        (SDA)-A4    D5-(PWM)        :M1/N1
//        (SCL)-A5    D4              :UP
//              A6    D3-(INT1)(PWM)  :CHB
//              A7    D2-(INT0)       :CHA
//              5V    GND
//              RST   RST
//              GND   RX0
//              VIN   TX1

#define CHA         2      // Quadrature encoder A pin
#define CHB         3      // Quadrature encoder B pin
#define M1          6      //maxon pwm output 1
#define M2          5      //maxon pwm output 2

#define UP          4
#define DOWN        7
#define HALFUP      10
#define HALFDOWN    8


double kp = 35 , ki = 1.0 , kd = 0.01;             // modify for optimal performance        //FIX
double input = 0, output = 0, setpoint = 0;
volatile long encoderPos = 0;

unsigned long current, previous, interval=30;
unsigned long current_m, previous_m, interval_m=100;
unsigned long current_mhd, previous_mhd, interval_mhd=100;
unsigned long current_mh, previous_mh, interval_mh=400;
PID myPID(&input, &output, &setpoint, kp, ki, kd, DIRECT);  // if motor will only run at full speed try 'REVERSE' instead of 'DIRECT'

void setup() {
  pinMode(CHA, INPUT_PULLUP);     
  pinMode(CHB, INPUT_PULLUP); 
  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(UP, INPUT_PULLUP);
  pinMode(DOWN, INPUT_PULLUP);
  pinMode(HALFUP, INPUT_PULLUP);
  pinMode(HALFDOWN, INPUT_PULLUP);
  attachInterrupt(0 ,count1,FALLING); 
  myPID.SetMode(AUTOMATIC);
  myPID.SetSampleTime(10);          //fixxxxxxxxxx*****************************
  myPID.SetOutputLimits(-255, 255);
  setpoint =0;                                      // modify to fit motor and encoder characteristics
  Serial.begin(115200);
   //TCCR1B = TCCR1B & 0b11111000 | 1;                    // set 31KHz PWM to prevent motor noise   FIXX!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  delay(2000);
}

void loop() {
 if (!digitalRead(UP)){Serial.println("UP");delay(1);maxon_up();}
 if (!digitalRead(DOWN)){Serial.println("DOWN");delay(1);maxon_down();}
 if (!digitalRead(HALFUP)){Serial.println("HALFUP");delay(1);maxon_up_half();}
 if (!digitalRead(HALFDOWN)){Serial.println("HALFDOWN");delay(1);maxon_down_half();}
// ptr();
 encoderPos=0;

}

void count1() {
 if (digitalRead(CHB)==HIGH)
    encoderPos--;
 else
    encoderPos++;
}


void maxon_up(){
  setpoint=14;                                                                           //FIX
  previous_m=millis();
  previous_m+=interval_m;
  while(1){
    current_m=millis();
    if(current_m>previous_m) {break;}
    input = encoderPos ;                                // data from encoder
    myPID.Compute();                                    // calculate new output
    pwmOut(output);
   // ptr();
  }
  setpoint=0;
  previous_m=millis();
  previous_m+=interval_m;
  while(1){
      current_m=millis();
      if(current_m>previous_m) {break;}
      input = encoderPos ;                                // data from encoder
      myPID.Compute();                                    // calculate new output
      pwmOut(output);
         // ptr();
  }
  
    output=0;
  analogWrite(M1, 0);
  analogWrite(M2, 0);
}     

void maxon_down(){
  setpoint=-14;                                                                              //FIX
  previous_m=millis();
  previous_m+=interval_m;
  while(1){
    current_m=millis();
    if(current_m>previous_m) {break;}
    input = encoderPos ;                                // data from encoder
    myPID.Compute();                                    // calculate new output
    pwmOut(output);
       // ptr();
  }
  setpoint=0;
  previous_m=millis();
  previous_m+=interval_m;
  while(1){
      current_m=millis();
      if(current_m>previous_m) {break;}
      input = encoderPos ;                                // data from encoder
      myPID.Compute();                                    // calculate new output
      pwmOut(output);
         // ptr();
  }
    output=0;
  analogWrite(M1, 0);
  analogWrite(M2, 0);     
}

void maxon_up_half(){
  //kp=30;
  setpoint=13;                                                                                             //FIX
  previous_mh=millis();
  previous_mh+=interval_mh;
  while(1){
    current_mh=millis();
    if(current_mh>previous_mh) {break;}
    input = encoderPos ;                                // data from encoder
    myPID.Compute();                                    // calculate new output
    pwmOut(output);
       // ptr();
  }
  setpoint=0;
  previous_mh=millis();
  previous_mh+=interval_mh;
  while(1){
      current_mh=millis();
      if(current_mh>previous_mh) {break;}
      input = encoderPos ;                                // data from encoder
      myPID.Compute();                                    // calculate new output
      pwmOut(output);
         // ptr();
  }
    output=0;
  analogWrite(M1, 0);
  analogWrite(M2, 0);  
 // kp=35;   
}
void maxon_down_half(){
  setpoint=-13;                                                                                             //FIX
  previous_mhd=millis();
  previous_mhd+=interval_mhd;
  while(1){
    current_mhd=millis();
    if(current_mhd>previous_mhd) {break;}
    input = encoderPos ;                                // data from encoder
    myPID.Compute();                                    // calculate new output
    pwmOut(output);
      //  ptr();
  }
  setpoint=0;
  previous_mh=millis();
  previous_mh+=interval_mh;
  while(1){
      current_mh=millis();
      if(current_mh>previous_mh) {break;}
      input = encoderPos ;                                // data from encoder
      myPID.Compute();                                    // calculate new output
      pwmOut(output);
        //  ptr();
  }
  output=0;
  analogWrite(M1, 0);
  analogWrite(M2, 0);     
}


void pwmOut(int out) {                                // to H-Bridge board
 if (out > 0) {
     analogWrite(M2, 0);

   analogWrite(M1, out);                             // drive motor CW
 }
 else {
   analogWrite(M1, 0);
   analogWrite(M2, abs(out));                        // drive motor CCW
 }
}

void ptr() {
   Serial.print(encoderPos);
 Serial.print(",");
 Serial.print(setpoint);
 Serial.print(",");
 Serial.println(output);
}

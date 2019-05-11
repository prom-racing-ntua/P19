#include <PID_v1.h>
#define CHA      5                       // Quadrature encoder A pin
#define CHB      6                       // Quadrature encoder B pin
#define M1              0                       // PWM outputs to L298N H-Bridge motor driver module
#define M2              1
#define button          4

double kp = 35 , ki = 2.3 , kd = 0.01;             // modify for optimal performance
double input = 0, output = 0, setpoint = 0;
long temp;
volatile long encoderPos = 0;

unsigned long current, previous, interval=800;

PID myPID(&input, &output, &setpoint, kp, ki, kd, DIRECT);  // if motor will only run at full speed try 'REVERSE' instead of 'DIRECT'

void setup() {
 pinMode(CHA, INPUT_PULLUP);                  // quadrature encoder input A 
 pinMode(CHB, INPUT_PULLUP);                  // quadrature encoder input B
 pinMode(button, INPUT_PULLUP);
 attachInterrupt(5 ,count1,FALLING);// update encoder position
// TCCR1B = TCCR1B & 0b11111000 | 1;                   // set 31KHz PWM to prevent motor noise
 myPID.SetMode(AUTOMATIC);
 myPID.SetSampleTime(10);
 myPID.SetOutputLimits(-255, 255);
 Serial.begin (115200);                              // for debugging
 setpoint = 0;                       // modify to fit motor and encoder characteristics, potmeter connected to A0
}

void loop() {
  
 input = encoderPos ;                                // data from encoder
 Serial.print(encoderPos);                      // monitor motor position
 myPID.Compute();                                    // calculate new output
 pwmOut(output);
 Serial.print("  -  ");
 Serial.print(output);// drive L298N H-Bridge module
 Serial.print("  -  ");
 Serial.println(setpoint);// drive L298N H-Bridge module    
  if(digitalRead(button)==LOW) {
    shiftup();
    delay(300);
  }
}

void pwmOut(int out) {                                // to H-Bridge board
 if (out > 0) {
   analogWrite(M1, out);                             // drive motor CW
   analogWrite(M2, 0);
 }
 else {
   analogWrite(M1, 0);
   analogWrite(M2, abs(out));                        // drive motor CCW
 }
}

void count1() {
 if (digitalRead(CHB)==HIGH){encoderPos++;}else{encoderPos--;}
}

void shiftup(){                       
  setpoint=-12;
  previous=millis();
  previous+=interval;
  while(1){
    current=millis();
    if(current>previous) {break;}
    input = encoderPos ;                                // data from encoder
    myPID.Compute();                                    // calculate new output
    pwmOut(output);
  }
  setpoint=0;
  previous=millis();
  previous+=interval;
  while(1){
      current=millis();
      if(current>previous) {break;}
      input = encoderPos ;                                // data from encoder
      myPID.Compute();                                    // calculate new output
      pwmOut(output);
  }
} 

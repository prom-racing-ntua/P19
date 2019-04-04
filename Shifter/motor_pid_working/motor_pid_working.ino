#include <PinChangeInt.h>
#include <PID_v1.h>
#define encodPinA1      2                       // Quadrature encoder A pin
#define encodPinB1      3                       // Quadrature encoder B pin
#define M1              5                       // PWM outputs to L298N H-Bridge motor driver module
#define M2              6

double kp = 27 , ki = 2.5 , kd = 0.01;             // modify for optimal performance
double input = 0, output = 0, setpoint = 0;
long temp;
volatile long encoderPos = 0;
PID myPID(&input, &output, &setpoint, kp, ki, kd, DIRECT);  // if motor will only run at full speed try 'REVERSE' instead of 'DIRECT'

void setup() {
 pinMode(encodPinA1, INPUT_PULLUP);                  // quadrature encoder input A 
 pinMode(encodPinB1, INPUT_PULLUP);                  // quadrature encoder input B
//  attachInterrupt(0, encoder, FALLING);
 attachInterrupt(digitalPinToInterrupt(3) ,count1,FALLING);// update encoder position
 TCCR1B = TCCR1B & 0b11111000 | 1;                   // set 31KHz PWM to prevent motor noise
 myPID.SetMode(AUTOMATIC);
 myPID.SetSampleTime(1);
 myPID.SetOutputLimits(-255, 255);
 Serial.begin (115200);                              // for debugging
 setpoint = -30;                       // modify to fit motor and encoder characteristics, potmeter connected to A0
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
 if((output<=1.5 )&& (output>=-1.7)) {
  setpoint=0;
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
 if (PINE & 0b00010000){encoderPos--;}else{encoderPos++;}
}

//Prom racing
//shifter 2019
//
//
//
//        (SCK)-D13   D12-(MISO)
//        3.3V  D11-(MOSI)(PWM)
//              REF   D10-(SS)(PWM)
//  CLUTCH:     A0    D9-(PWM)    :SERVO_SIG
//  SHIFT_UP:   A1    D8
//SHIFT_DOWN:   A2    D7
//              A3    D6-(PWM)    :M2/N2
//        (SDA)-A4    D5-(PWM)    :M1/N1
//        (SCL)-A5    D4        :SPARKCUT
//              A6    D3-(INT1)(PWM)  :CHB
//              A7    D2-(INT0)   :CHA
//              5V    GND
//              RST   RST
//              GND   RX0
//              VIN   TX1


//vres pos allazoume to clock (gia to moter 31kHz)
// to setpoint prepei na to doume ligo....borei na iparxei kai kaliteros tropos na to allazoume
//episis to autoshift thelei ena check
// kai na milisei me ECU na doume ti dinei to tps kai ta loipa!
//genika ta pins einai ok maparismena...

#include <PID_v1.h>
#include <SPI.h>
#include "mcp_can.h"
#include <Servo.h> 

//clutch variables
#define pot_clutch_MIN 92   //Fix   
#define pot_clutch_MAX 270   //Fix
#define pot_error 15

//delays
#define clutch_t    100    //wait the servo!
#define spark_delay  10    //wait the ECU!

//pins
#define CHA         2      // Quadrature encoder A pin
#define CHB         3      // Quadrature encoder B pin
#define M1          5      //maxon pwm output 1
#define M2          6      //maxon pwm output 2
//#define led_up      A5     //shift up indication
//#define led_down    A6     //shift down indication
//#define led_clutch  A1     //clutch indication
#define sparkcut    4      //Gearcut pin at ECU
#define shift_up    A1      //steering wheel right pad(shift up)
#define shift_down  A2      //steering wheel left pad(shift down)
#define neutral     14
#define servo_pin   9      //servo signal
#define total_gears 5

//pid variables
double kp = 40 , ki = 2.3 , kd = 0.01;             // modify for optimal performance        //FIX
double input = 0, output = 0, setpoint = 0;
volatile long encoderPos = 0;

//general variables
unsigned long current, previous, interval=30;
unsigned long current_m, previous_m, interval_m=200;
uint16_t pot_pos, clutch_pos;
uint8_t shift_flag=1;

//CANBUS variables
uint8_t launch=0, neutral_prev=0;
int gear=0;


PID myPID(&input, &output, &setpoint, kp, ki, kd, DIRECT);  // if motor will only run at full speed try 'REVERSE' instead of 'DIRECT'
Servo clutch;

void setup() {
  Serial.begin(115200);
  pinMode(shift_down, INPUT_PULLUP);
  pinMode(shift_up, INPUT_PULLUP);
  pinMode(neutral, INPUT_PULLUP);
  pinMode(CHA, INPUT_PULLUP);     
  pinMode(CHB, INPUT_PULLUP); 
  pinMode(sparkcut, OUTPUT);
  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);
//  pinMode(led_up, OUTPUT);
//  pinMode(led_down, OUTPUT);
//  pinMode(led_clutch, OUTPUT);
  
  clutch.attach(servo_pin, 1000, 1600);               // 1000->1600ms = 0->60 degrees      FIX
  clutch.writeMicroseconds(1000);                      // initialize servo's position               FIX
  attachInterrupt(1 ,count1,FALLING);                  // encoder interrupt
  //TCCR1B = TCCR1B & 0b11111000 | 1;                    // set 31KHz PWM to prevent motor noise   FIXX!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  myPID.SetMode(AUTOMATIC);
  myPID.SetSampleTime(10);          //fixxxxxxxxxx*****************************
  myPID.SetOutputLimits(-255, 255);
  setpoint =0;                                      // modify to fit motor and encoder characteristics
  
}

void loop() {

  current=millis();
  pot_pos = analogRead(A0);  //steering wheel clutch potentiometer
  
  Serial.print("Gear: ");
  Serial.print(gear);
  Serial.print("   pot_position: ");
  Serial.print(pot_pos);
  Serial.print("  clutch_pos:  ");
  Serial.println(clutch_pos);
  
  //check if the clutch is pressed
  if(pot_pos<(pot_clutch_MIN+pot_error)) {   //the clutch is not pressed
     clutch.writeMicroseconds(1480);                                                                                                         //why?
     //digitalWrite(led_clutch, LOW);
     if((shift_flag==1) && (digitalRead(shift_up)==LOW)&& gear!=0) { //up shift
           gear++;
           if(gear <= total_gears)  {    //check if we passed the total number of gears
              digitalWrite(sparkcut, HIGH);
              delay(spark_delay);
              maxon_up();
              digitalWrite(sparkcut, LOW);
           }
           else {gear=5;}
           shift_flag=0;
           previous=millis();
           previous +=interval;
      }
      if(shift_flag==1 && (digitalRead(shift_down)==LOW) && gear!=0) {
          gear--;
          if(gear>=1) {    
             clutch.writeMicroseconds(1200);
             //digitalWrite(led_clutch, HIGH);
             delay(clutch_t);
             maxon_down();
             clutch.writeMicroseconds(1480);
             //digitalWrite(led_clutch, LOW);
                   
          }
          else {gear=1;}
          shift_flag=0;
          previous=millis();
          previous +=interval;
        }
  
  }
  else if(pot_pos>pot_clutch_MIN && pot_pos<pot_clutch_MAX){ //the clutch is pressed
    //digitalWrite(led_clutch, HIGH);
    //move servo
    clutch_pos = supermap(pot_pos, pot_clutch_MIN, pot_clutch_MAX, 1600, 1000);
    clutch.writeMicroseconds(clutch_pos);
   
    if((digitalRead(shift_up)==LOW) && shift_flag==1){      
        gear++;
        if(gear==0) {
            clutch.writeMicroseconds(1200);
            delay(clutch_t);
            maxon_down_half();
            clutch.writeMicroseconds(clutch_pos);
        }
        else if(gear <= total_gears)  {
            clutch.writeMicroseconds(1200);
            delay(clutch_t);
            maxon_up();
            clutch.writeMicroseconds(clutch_pos);
        }
        else{gear=5;}
        shift_flag=0;
        previous=millis();
        previous +=interval;
    }
    if((digitalRead(shift_down)==LOW) && shift_flag==1){        
        gear--;
        if(gear>0) {
           clutch.writeMicroseconds(1200);
           delay(clutch_t);
           maxon_down();
           clutch.writeMicroseconds(clutch_pos);
        }
        else if(gear==0) {
           clutch.writeMicroseconds(1200);
           delay(clutch_t);
           maxon_up_half();
           clutch.writeMicroseconds(clutch_pos);
        }
        else{gear=0;}
        shift_flag=0;
        previous=millis();
        previous +=interval;
    }
   
//   if(digitalRead(neutral)==LOW && neutral_prev==0) { 
//      //clutch.writeMicroseconds(1200);
//      delay(clutch_t);
//      for(int i=0; i<gear-2; i++) {                  //shift down all the way to second gear
//          maxon_down();
//          delay(100);                             //borei kai ligotero
//      }
//      maxon_down_half();                           //shift down half  to neutral
//      //clutch.writeMicroseconds(clutch_pos);
//      gear=0;
//      neutral_prev=1;
//   }
//  }  
  
//  if(digitalRead(neutral)==HIGH) {
//    neutral_prev=0;
//  }
}

if(current>previous){   //Debouncing method
    if(digitalRead(shift_up)==HIGH  && digitalRead(shift_down)==HIGH){ //means we have released both shifting pads
       shift_flag=1;
    }
  }

}
int supermap(double pot_pos,double pot_clutch_min,double pot_clutch_max,double servo_max,double servo_min) {
  int clutch_pos;
  uint8_t n=5;
  clutch_pos=servo_max+(servo_min-servo_max)*(pow((pot_clutch_min/pot_pos),n)-1)/(pow((pot_clutch_min/pot_clutch_max),n)-1);
  return clutch_pos;
}

void count1() {
 if (digitalRead(CHA)==LOW)
    encoderPos--;
 else
    encoderPos++;
}

void maxon_up(){
  setpoint=-12;                                                                           //FIX
  previous_m=millis();
  previous_m+=interval_m;
  while(1){
    current_m=millis();
    if(current_m>previous_m) {break;}
    input = encoderPos ;                                // data from encoder
    myPID.Compute();                                    // calculate new output
    pwmOut(output);
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
  }
//  analogWrite(M1, 0);
//  analogWrite(M2, 0);
}     

void maxon_down(){
  setpoint=12;                                                                              //FIX
  previous_m=millis();
  previous_m+=interval_m;
  while(1){
    current_m=millis();
    if(current_m>previous_m) {break;}
    input = encoderPos ;                                // data from encoder
    myPID.Compute();                                    // calculate new output
    pwmOut(output);
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
  }
//  analogWrite(M1, 0);
//  analogWrite(M2, 0);     
}

void maxon_up_half(){
  setpoint=-6;                                                                                             //FIX
  previous_m=millis();
  previous_m+=interval_m;
  while(1){
    current_m=millis();
    if(current_m>previous_m) {break;}
    input = encoderPos ;                                // data from encoder
    myPID.Compute();                                    // calculate new output
    pwmOut(output);
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
  }
//  analogWrite(M1, 0);
//  analogWrite(M2, 0);     
}
void maxon_down_half(){
  setpoint=6;                                                                                             //FIX
  previous_m=millis();
  previous_m+=interval_m;
  while(1){
    current_m=millis();
    if(current_m>previous_m) {break;}
    input = encoderPos ;                                // data from encoder
    myPID.Compute();                                    // calculate new output
    pwmOut(output);
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
  }
//  analogWrite(M1, 0);
//  analogWrite(M2, 0);     
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

//Prom racing
//shifter 2019

/*              :AREF      5V: 
 *              :DAC      VIN:
 *    AUX3      :A1      3.3V:
 * CLUTCH       :Α2       GND:
 * SHIFT_UP     :Α3     RESET:
 *SHIFT_DOWN    :Α4        14:  (TX):  AUX1
 *       N1     :Α5        13:  (RX):  AUX2
 *       N2     :Α6        12:  (SCL)
 *       M1     :0         11:  (SDA)
 *       M2     :1         10:  (MISO)
 *SERVO_SIG     :2          9:  (SCK)
 *RESERVED(CAN) :3          8:  (MOSI)
 * SPARKCUT     :4          7:   RESERVED(CAN)
 *        CHA   :5          6:   CHB
 */

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
#define pot_clutch_MIN 200   //Fix   
#define pot_clutch_MAX 873   //Fix
#define pot_error 15

//delays
#define clutch_t    100    //wait the servo!
#define spark_delay  10    //wait the ECU!

//pins
#define CHA         5      // Quadrature encoder A pin
#define CHB         6      // Quadrature encoder B pin
#define M1          0      //maxon pwm output 1
#define M2          1      //maxon pwm output 2
//#define led_up      A5     //shift up indication
//#define led_down    A6     //shift down indication
//#define led_clutch  A1     //clutch indication
#define sparkcut    4      //Gearcut pin at ECU
#define shift_up    A3      //steering wheel right pad(shift up)
#define shift_down  A4      //steering wheel left pad(shift down)
//#define neutral     14
#define clutch_pin  2      //servo signal
#define total_gears 5

//pid variables
double kp = 40 , ki = 2.3 , kd = 0.01;             // modify for optimal performance        //FIX
double input = 0, output = 0, setpoint = 0;
volatile long encoderPos = 0;

//general variables
unsigned long current, previous, interval=30;
unsigned long current_m, previous_m, interval_m=90;
uint16_t pot_pos, clutch_pos;
uint8_t shift_flag=1;

//CANBUS variables
uint8_t launch=0, neutral_prev=0;
int gear=0;


//autoshift variables
int n2[total_gears]={9500, 9500, 9500, 9500, 20000};
int n_accel[total_gears]={0, 2500, 3000, 3500, 4800};
int n_brake[total_gears]={0, 3000, 3600, 4500, 5600};
int tps_min=5, tps_max=90;                          // pososto petaloudas !!!       prosoxi prepei na doume se ti morfi to dinei i ecu!!!

//launch control variables
uint8_t launch_cancel=0;

const int SPI_CS_PIN = 3;
//MCP_CAN CAN(SPI_CS_PIN);
PID myPID(&input, &output, &setpoint, kp, ki, kd, DIRECT);  // if motor will only run at full speed try 'REVERSE' instead of 'DIRECT'
Servo clutch;

void setup() {
  Serial.begin(115200);
//  CAN.begin(CAN_1000KBPS);                           // 1Mbps
  pinMode(shift_down, INPUT_PULLUP);
  pinMode(shift_up, INPUT_PULLUP);
  pinMode(CHA, INPUT_PULLUP);     
  pinMode(CHB, INPUT_PULLUP); 
  pinMode(sparkcut, OUTPUT);
  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);

  
  clutch.attach(clutch_pin, 1000, 1600);               // 1000->1600ms = 0->60 degrees      FIX
  clutch.writeMicroseconds(1000);                      // initialize servo's position               FIX
  attachInterrupt(5 ,count1,FALLING);                  // encoder interrupt
  //TCCR1B = TCCR1B & 0b11111000 | 1;                    // set 31KHz PWM to prevent motor noise   FIXX!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  myPID.SetMode(AUTOMATIC);
  myPID.SetSampleTime(10);      //fixxxxxx************************
  myPID.SetOutputLimits(-255, 255);
  setpoint =0;                                      // modify to fit motor and encoder characteristics
  
}

void loop() {
  current=millis();
  pot_pos = analogRead(A2);  //steering wheel clutch potentiometer
    Serial.print("Gear: ");
  Serial.print(gear);
  Serial.print("   pot_position: ");
  Serial.print(pot_pos);
  Serial.print("  clutch_pos:  ");
  Serial.println(clutch_pos);
  
  
  //check if the clutch is pressed
  if(pot_pos<(pot_clutch_MIN+pot_error)) {   //the clutch is not pressed
     clutch.writeMicroseconds(1480);                                                                                                         //why?
//     digitalWrite(led_clutch, LOW);
     if((shift_flag==1) && gear!=0 && (digitalRead(shift_up)==LOW)) { //up shift
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
             delay(clutch_t);
             maxon_down();
             clutch.writeMicroseconds(1480);
                   
          }
          else {gear=1;}
          shift_flag=0;
          previous=millis();
          previous +=interval;
        }
  
  }
  else if(pot_pos>pot_clutch_MIN && pot_pos<pot_clutch_MAX+pot_error){ //the clutch is pressed
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
//      clutch.writeMicroseconds(1200);
//      delay(clutch_t);
//      for(int i=0; i<gear-2; i++) {                  //shift down all the way to second gear
//          maxon_down();
//          delay(100);                             //borei kai ligotero
//      }
//      maxon_down_half();                           //shift down half  to neutral
//      clutch.writeMicroseconds(clutch_pos);
//      gear=0;
//      neutral_prev=1;
//   }
  }  
  if(current>previous){   //Debouncing method
    if(digitalRead(shift_up)==HIGH  && digitalRead(shift_down)==HIGH){ //means we have released both shifting pads
       shift_flag=1;
    }
  }
//  if(digitalRead(neutral)==HIGH) {
//    neutral_prev=0;
//  }
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
  analogWrite(M1, 0);
  analogWrite(M2, 0);
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
      output=0;
  analogWrite(M1, 0);
  analogWrite(M2, 0);
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
  analogWrite(M1, 0);
  analogWrite(M2, 0);
  previous_m=millis();
  previous_m+=interval_m;
  while(1){
      current_m=millis();
      if(current_m>previous_m) {break;}
      input = encoderPos ;                                // data from encoder
      myPID.Compute();                                    // calculate new output
      pwmOut(output);
  }
      output=0;
  analogWrite(M1, 0);
  analogWrite(M2, 0);     
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
  analogWrite(M1, 0);
  analogWrite(M2, 0);
  previous_m=millis();
  previous_m+=interval_m;
  while(1){
      current_m=millis();
      if(current_m>previous_m) {break;}
      input = encoderPos ;                                // data from encoder
      myPID.Compute();                                    // calculate new output
      pwmOut(output);
  }
      output=0;
  analogWrite(M1, 0);
  analogWrite(M2, 0);     
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
  analogWrite(M1, 0);
  analogWrite(M2, 0);
  previous_m=millis();
  previous_m+=interval_m;
  while(1){
      current_m=millis();
      if(current_m>previous_m) {break;}
      input = encoderPos ;                                // data from encoder
      myPID.Compute();                                    // calculate new output
      pwmOut(output);
  }
      output=0;
  analogWrite(M1, 0);
  analogWrite(M2, 0);     
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

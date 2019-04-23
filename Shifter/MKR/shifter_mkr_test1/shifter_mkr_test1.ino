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
#define pot_clutch_MIN 300   //Fix   
#define pot_clutch_MAX 900   //Fix
#define pot_error 15

//delays
#define clutch_t    100    //wait the servo!
#define spark_delay  10    //wait the ECU!

//pins
#define CHA         5      // Quadrature encoder A pin
#define CHB         6      // Quadrature encoder B pin
#define M1          0      //maxon pwm output 1
#define M2          1      //maxon pwm output 2
#define led_up      A5     //shift up indication
#define led_down    A6     //shift down indication
#define led_clutch  A1     //clutch indication
#define sparkcut    4      //Gearcut pin at ECU
#define shift_up    A3      //steering wheel right pad(shift up)
#define shift_down  A4      //steering wheel left pad(shift down)
#define newtral     14
#define clutch_pin  2      //servo signal
#define total_gears 5

//pid variables
double kp = 27 , ki = 2.5 , kd = 0.01;             // modify for optimal performance        //FIX
double input = 0, output = 0, setpoint = 0;
volatile long encoderPos = 0;

//general variables
unsigned long current, previous, interval=30;
uint16_t pot_pos, clutch_pos;
uint8_t shift_flag=1;

//CANBUS variables
uint8_t launch=0, newtral_prev=0;
int gear=0;


//autoshift variables
int n2[total_gears]={9500, 9500, 9500, 9500, 99999};
int n_accel[total_gears]={0, 2500, 3000, 3500, 4800};
int n_brake[total_gears]={0, 3000, 3600, 4500, 5600};
int tps_min=5, tps_max=90;                          // pososto petaloudas !!!       prosoxi prepei na doume se ti morfi to dinei i ecu!!!

//launch control variables
uint8_t launch_cancel=0;

const int SPI_CS_PIN = 3;
MCP_CAN CAN(SPI_CS_PIN);
PID myPID(&input, &output, &setpoint, kp, ki, kd, DIRECT);  // if motor will only run at full speed try 'REVERSE' instead of 'DIRECT'
Servo clutch;

void setup() {
  Serial.begin(115200);
  CAN.begin(CAN_1000KBPS);                           // 1Mbps
  pinMode(shift_down, INPUT_PULLUP);
  pinMode(shift_up, INPUT_PULLUP);
  pinMode(newtral, INPUT_PULLUP);
  pinMode(CHA, INPUT_PULLUP);     
  pinMode(CHB, INPUT_PULLUP); 
  pinMode(sparkcut, OUTPUT);
  //pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(led_up, OUTPUT);
  pinMode(led_down, OUTPUT);
  pinMode(led_clutch, OUTPUT);
  
  clutch.attach(clutch_pin, 1000, 1600);               // 1000->1600ms = 0->60 degrees      FIX
  clutch.writeMicroseconds(1000);                      // initialize servo's position               FIX
  
  //attachInterrupt(5 ,count1,FALLING);                  // encoder interrupt
  //TCCR1B = TCCR1B & 0b11111000 | 1;                    // set 31KHz PWM to prevent motor noise   FIXX!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  myPID.SetMode(AUTOMATIC);
  myPID.SetSampleTime(1);
  myPID.SetOutputLimits(-255, 255);
  setpoint = -30;                                      // modify to fit motor and encoder characteristics
  
}

void loop() {
  current=millis();
  pot_pos = analogRead(A2);
  
  //check if the clutch is pressed
  if(pot_pos<(pot_clutch_MIN-pot_error)) {   //the clutch is not pressed
     //clutch.writeMicroseconds(1480);                                                      //why?
     digitalWrite(led_clutch, LOW);
     if((digitalRead(shift_up)==LOW) && (shift_flag==1) && gear!=0) { //up shift
           gear++;
           if(gear <= total_gears)  {    //check if we passed the total number of gears
              digitalWrite(sparkcut, HIGH);
              delay(spark_delay);
              digitalWrite(led_up, HIGH);
              delay(300);
              digitalWrite(led_up, LOW);
              digitalWrite(sparkcut, LOW);
           }
           else {gear=5;}
           shift_flag=0;
           previous=millis();
           previous +=interval;
      }
      if((digitalRead(shift_down)==LOW) && shift_flag==1) {
          gear--;
          if(gear>=1) {    
             clutch.writeMicroseconds(1200);
             digitalWrite(led_clutch, HIGH);
             delay(clutch_t); 
              digitalWrite(led_down, HIGH);
              delay(300);
              digitalWrite(led_down, LOW);
             clutch.writeMicroseconds(1480);
             digitalWrite(led_clutch, LOW);
                   
          }
          else {gear=1;}
          shift_flag=0;
          previous=millis();
          previous +=interval;
        }
  
  }
  else if(pot_pos>pot_clutch_MIN && pot_pos<pot_clutch_MAX){ //the clutch is pressed
    digitalWrite(led_clutch, HIGH);
    //move servo
    clutch.writeMicroseconds(clutch_pos);
   
    if((digitalRead(shift_up)==LOW) && shift_flag==1){      
        gear++;
        if(gear <= total_gears)  {
            clutch.writeMicroseconds(1200);
            delay(clutch_t);            
            digitalWrite(led_up, HIGH);
            delay(300);
            digitalWrite(led_up, LOW);
            clutch.writeMicroseconds(clutch_pos);
        }
        else{gear=5;}
        shift_flag=0;
        previous=millis();
        previous +=interval;
    }
    if((digitalRead(shift_down)==LOW) && shift_flag==1){        
        gear--;
        if(gear>=0) {
           clutch.writeMicroseconds(1200);
           delay(clutch_t);
            digitalWrite(led_down, HIGH);
            delay(300);
            digitalWrite(led_down, LOW);
            clutch.writeMicroseconds(clutch_pos);
        }
        else{gear=0;}
        shift_flag=0;
        previous=millis();
        previous +=interval;
    }
   
   if(digitalRead(newtral)==LOW && newtral_prev==0) { 
      clutch.writeMicroseconds(1200);
      delay(clutch_t);
          while(gear>0){  //shift down all the way to neutral
            digitalWrite(led_down, HIGH);
            delay(300);
            digitalWrite(led_down, LOW);
            delay(200);
            gear--;
          }
      //}
      clutch.writeMicroseconds(clutch_pos);
      gear=0;
      newtral_prev=1;
   }
  } 
  if(current>previous){   //Debouncing method
    if(digitalRead(shift_up)==HIGH  && digitalRead(shift_down)==HIGH){ //means we have released both shifting pads
       shift_flag=1;
    }
  }
  if(digitalRead(newtral)==HIGH) {
    newtral_prev=0;
  }
}

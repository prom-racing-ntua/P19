//Prom racing
//shifter 2019

/*              :AREF      5V: 
 *              :DAC      VIN:
 *    AUX3      :A1      3.3V:
 * CLUTCH       :Α2       GND:
 * SHIFT_UP     :Α3     RESET:
 *SHIFT_DOWN    :Α4        14:  (TX)
 *       N1     :Α5        13:  (RX):  AUX1
 *       N2     :Α6        12:  (SCL): AUX2
 *       M1     :0         11:  (SDA)
 *       M2     :1         10:  (MISO)
 *SERVO_SIG     :2          9:  (SCK)
 *RESERVED(CAN) :3          8:  (MOSI)
 * SPARKCUT     :4          7:   RESERVED(CAN)
 *        CHA   :5          6:   CHB
 */

//vres pos allazoume to clock (gia to moter 31kHz)
// to setpoint prepei na to doume ligo....borei na iparxei kai kaliterow tropos na to allazoume
//episis to autoshift thelei ena check
// kai na milisei me ECU na doume ti dinei to tps kai ta loipa!
//genika ta pins einai ok maparismena...


//#include <PinChangeInt.h>
#include <PID_v1.h>
#include <SPI.h>
#include "mcp_can.h"
#include <Servo.h> 

//clutch variables
#define pot_clutch_MIN 206   //Fix   
#define pot_clutch_MAX 390   //Fix
#define pot_error 15

//delays
#define clutch_t    100    //wait the servo!
#define spark_delay 10     //wait the ECU!

//pins
#define CHA         5      // Quadrature encoder A pin
#define CHB         6      // Quadrature encoder B pin
#define M1          0      //maxon pwm output 1
#define M2          1      //maxon pwm output 2
#define sparkcut    4      //Gearcut pin at ECU
#define shift_up   18      //steering wheel right pad(shift up)
#define shift_down 19      //steering wheel left pad(shift down)
#define clutch_pin  2      //servo signal
#define total_gears 5

//pid variables
double kp = 27 , ki = 2.5 , kd = 0.01;             // modify for optimal performance        //FIX
double input = 0, output = 0, setpoint = 0;
volatile long encoderPos = 0;

//general variables
unsigned long current, previous, interval;
uint16_t pot_pos, clutch_pos;
uint8_t shift_flag=1;

//CANBUS variables
uint8_t launch=0, autoshift=0, neutral=0, rpm=0, tps=0;
unsigned char len = 0;
unsigned char buf[8];

//autoshift variables
int n2[total_gears]={9500, 9500, 9500, 9500, 99999};
int n_accel[total_gears]={0, 2500, 3000, 3500, 4800};
int n_brake[total_gears]={0, 3000, 3600, 4500, 5600};
int tps_min=5, tps_max=90;                          // pososto petaloudas !!!       prosoxi prepei na doume se ti morfi to dinei i ecu!!!
uint8_t gear=0;

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
  myPID.SetSampleTime(1);
  myPID.SetOutputLimits(-255, 255);
  setpoint = -30;                                      // modify to fit motor and encoder characteristics

  attachInterrupt(7, canReads, FALLING);               // CAN BUS interrupt
  
  CAN.init_Mask(0, 0, 0x3ff);                          // there are 2 mask in mcp2515, you need to set both of them
  CAN.init_Mask(1, 0, 0x3ff);                          // !!logika thelei allagi to mask!!
    
  CAN.init_Filt(0, 0, 0x334);                          // front left hall
  CAN.init_Filt(1, 0, 0x335);                          // front right hall
  CAN.init_Filt(2, 0, 0x06);                           // rear hall (right)
  CAN.init_Filt(3, 0, 0x07);                           // launch button + neutral button + autoshift button
  CAN.init_Filt(4, 0, 0x08);                           // ecu rpm & tps
  CAN.init_Filt(5, 0, 0x09);                           // gear!!
  interval=30;
}

void loop() {
  current=millis();
  pot_pos = analogRead(A2);
  
  //check if the clutch is pressed
  if(pot_pos<(pot_clutch_MIN-pot_error)) {   //the clutch is not pressed
     clutch.writeMicroseconds(1480);                                                      //why?
     
     if((digitalRead(shift_up)==LOW) && (shift_flag==1) || (autoshift==1 && rpm>n2[gear])) { //up shift
           gear++;
           if(gear <= total_gears)  {    //check if we passed the total number of gears
              digitalWrite(sparkcut, HIGH);
              delay(spark_delay);
              maxon_up();
              digitalWrite(sparkcut, LOW);
           }
           else {gear=5;}
           shift_flag=0;
           current=millis();
           previous=current;
           previous +=interval;
      }
      if((digitalRead(shift_down)==LOW) && shift_flag==1 || ((autoshift==1 && rpm<n2[gear] && tps<=tps_min) && (rpm<=n_brake[gear] || (tps>=tps_max && rpm<=n_accel[gear])))) {
          gear--;
          if(gear>=1) {    
             clutch.writeMicroseconds(1200);
             delay(clutch_t);
             maxon_down();
             clutch.writeMicroseconds(1480);
                   
          }
          else {gear=0;}
          shift_flag=0;
          current=millis();
          previous=current;
          previous +=interval;
        }
  
  }
  else if(pot_pos>pot_clutch_MIN && pot_pos<pot_clutch_MAX){ //the clutch is pressed

    //move servo
    clutch_pos = supermap(pot_pos, pot_clutch_MIN, pot_clutch_MAX, 1480, 1200);
    clutch.writeMicroseconds(clutch_pos);
    
    if((digitalRead(shift_up)==LOW) && shift_flag==1){      
        gear++;
        if(gear <= total_gears)  {
            clutch.writeMicroseconds(1200);
            delay(clutch_t);
            maxon_up();
            clutch.writeMicroseconds(clutch_pos);
        }
        else{gear=5;}
        shift_flag=0;
        current=millis();
        previous=current;
        previous +=interval;
    }
    if((digitalRead(shift_down)==LOW) && shift_flag==1){        
        gear--;
        if(gear>=1) {
           clutch.writeMicroseconds(1200);
           delay(clutch_t);
           maxon_down();
           clutch.writeMicroseconds(clutch_pos);
        }
        else{gear=0;}
        shift_flag=0;
        current=millis();
        previous=current;
        previous +=interval;
    }
    if(launch==1) {
      pot_pos = analogRead(A2);  //mallon oxi
      //LAUNCH SEQUENCE
      while(1){                    
            if(pot_pos<(pot_clutch_MIN-pot_error)) { //clutch not presed but launch button is still presed
                if(launch==0) break;                //launch button is released!!
           }
           else {                                   //clutch is presed && launch button is presed
              if(launch==0){ 
                 launch_cancel=1;                   //check if launch button is released before fully releasing the clutch!!! that means that we cancel the launch control!!!!!!!!!!
                 break;
              }
           }
           pot_pos = analogRead(A2);             //check clutch position
      }
      while(pot_pos<(pot_clutch_MIN-pot_error) && launch_cancel==0){   //clutch is not pressed && launch has not been canceled //na boun kai alles sinthikes gia asfaleia!!!!!!!!!!!!!!!!!!!
        pot_pos = analogRead(A2);              //check clutch position             pooooli argooo!! thelei allo tropo elegxou
        //launch code!
      
      
      }
      launch=0;
      launch_cancel=0;                                  
   }
   if(neutral==1) {
      clutch.writeMicroseconds(1200);
      delay(clutch_t);
      for(int i=0; i<gear; i++) {                  //shift down all the way to neutral
          maxon_down();
      }
      clutch.writeMicroseconds(clutch_pos);
      gear=0;
      neutral=0;
   }
  } 
  if(current>previous){   //Debouncing method
    if(digitalRead(shift_up)==HIGH  && digitalRead(shift_down)==HIGH){ //means we have released both shifting pads
       shift_flag=1;
    }
  }
}

int supermap(double pot_pos,double pot_clutch_min,double pot_clutch_max,double servo_max,double servo_min) {
  int clutch_pos;
  int n=5;
  clutch_pos=servo_max+(servo_min-servo_max)*(pow((pot_clutch_min/pot_pos),n)-1)/(pow((pot_clutch_min/pot_clutch_max),n)-1);
  return clutch_pos;
}

void canReads() {
  CAN.readMsgBuf(&len, buf);    // read data,  len: data length, buf: data buf
  if(CAN.getCanId()==820) { //decimal value of canid      // FIX ADDRESS
    if(bitRead(buf[7], 0)==1)  //FIX BIT!! 
      launch=1;
    if(bitRead(buf[6], 0)==1) //FIX BIT!!
      autoshift=1;
    else
      autoshift=0;
    if(bitRead(buf[5], 0)==1) //FIX BIT!!
       neutral=1;
    }
    else if(CAN.getCanId()==821) {
      tps=buf[7];            //FIX BIT!! // den einai toso aplo...thelei kati akoma!!!
      rpm=buf[6];            //FIX BIT!!
    }
}



void count1() {
 if (digitalRead(CHA)==LOW)
    encoderPos--;
 else
    encoderPos++;
}

void maxon_up(){
  setpoint=30;
  while((output<=1.7 )&& (output>=-1.7)){                //FIXXXXX!!!!!!!!!!!!!!
    input = encoderPos ;                                // data from encoder
    myPID.Compute();                                    // calculate new output
    pwmOut(output);
  }
  setpoint=0;
  while((output<=1.7 )&& (output>=-1.7)){
      input = encoderPos ;                                // data from encoder
      myPID.Compute();                                    // calculate new output
      pwmOut(output);
  }
}     

void maxon_down(){                       //FIX
  setpoint=-30;
  while((output<=1.7 )&& (output>=-1.7)){
    input = encoderPos ;                                // data from encoder
    myPID.Compute();                                    // calculate new output
    pwmOut(output);
  }
  setpoint=0;
  while((output<=1.7 )&& (output>=-1.7)){
      input = encoderPos ;                                // data from encoder
      myPID.Compute();                                    // calculate new output
      pwmOut(output);
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

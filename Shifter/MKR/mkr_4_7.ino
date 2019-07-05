unsigned char vibe_debounce = 150;


/*              :AREF      5V: 
 *              :DAC      VIN:
 *    AUX3      :A1      3.3V:
 * CLUTCH       :Α2       GND:
 * SHIFT_UP     :Α3     RESET:
 *SHIFT_DOWN    :Α4        14:  (TX):  AUX1
 *       N1     :Α5        13:  (RX):  AUX2
 *       N2     :Α6        12:  (SCL): HALFUP
 *       UP     :0         11:  (SDA):  HALFDOWN
 *     DOWN     :1         10:  (MISO)
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

#include <SPI.h>
#include "mcp_can.h"
#include <Servo.h> 

//clutch variables
#define pot_clutch_MIN 230   //Fix   
#define pot_clutch_MAX 844   //Fix
#define pot_error 15

//delays
#define clutch_t    100    //wait the servo!
#define spark_delay  20    //wait the ECU!
#define FULL        100
#define HALF        500

//pins
#define sparkcut    4      //Gearcut pin at ECU
#define shift_up    A3      //steering wheel right pad(shift up)
#define shift_down  A4      //steering wheel left pad(shift down)
//#define neutral     14
#define clutch_pin  2      //servo signal
#define total_gears 5

#define UP          0
#define DOWN        1
#define HALFUP      12
#define HALFDOWN    11


//general variables
unsigned long current, previous, interval=300;
uint16_t pot_pos, clutch_pos;
uint8_t shift_flag=1;
//CANBUS variables
volatile uint8_t launch=0, autoshift=0, neutral=0;
volatile uint8_t launch_prev=0, neutral_prev=0;
unsigned char len = 0;
unsigned char buf[8];
volatile uint8_t gear=0, tps=0, rr=0, rl=0, fr=0, fl=0;
volatile uint16_t rpm=0;



//autoshift variables
int n2[total_gears]={9500, 9500, 9500, 9500, 20000};
int n_accel[total_gears]={0, 2500, 3000, 3500, 4800};
int n_brake[total_gears]={0, 3000, 3600, 4500, 5600};
int tps_min=5, tps_max=90;                          // pososto petaloudas !!!       prosoxi prepei na doume se ti morfi to dinei i ecu!!!

//launch control variables
uint8_t launch_cancel=0;

const int SPI_CS_PIN = 3;
MCP_CAN CAN(SPI_CS_PIN);
Servo clutch;
unsigned long button_vibes_up=0;
unsigned long button_vibes_down=0;
unsigned char vibes_up=0;
unsigned char vibes_down=0;

void setup() {
  Serial.begin(115200);
  CAN.begin(CAN_1000KBPS);                           // 1Mbps
  
  pinMode(shift_down, INPUT_PULLUP);
  pinMode(shift_up, INPUT_PULLUP);
  pinMode(sparkcut, OUTPUT);
  pinMode(UP, OUTPUT);
  pinMode(DOWN, OUTPUT);
  pinMode(HALFUP, OUTPUT);
  pinMode(HALFDOWN, OUTPUT);

  clutch.attach(clutch_pin, 1000, 1600);               // 1000->1600ms = 0->60 degrees      FIX
  clutch.writeMicroseconds(1000);                      // initialize servo's position               FIX

 digitalWrite(UP, HIGH);
  digitalWrite(DOWN, HIGH);
   digitalWrite(HALFUP, HIGH);
    digitalWrite(HALFDOWN, HIGH);
digitalWrite(sparkcut,HIGH);
              
// attachInterrupt(7, canReads, FALLING);               // CAN BUS interrupt
//  
//  CAN.init_Mask(0, 0, 0x000);                          // there are 2 mask in mcp2515, you need to set both of them
//  CAN.init_Mask(1, 0, 0xfff);                          // !!logika thelei allagi to mask!!
//    
//  CAN.init_Filt(0, 0, 0x5fc);                          // rear right hall
//  CAN.init_Filt(1, 0, 0x5fd);                          // rear left hall
//  CAN.init_Filt(2, 0, 0x5fe);                          // front right hall
//  CAN.init_Filt(3, 0, 0x600);                          // ecu rpm &tps
//  CAN.init_Filt(4, 0, 0x604);                          // ecu gear
//  CAN.init_Filt(5, 0, 0x666);                          // launch button + neutral button + autoshift button
//    
}

void loop() {
  if(CAN_MSGAVAIL == CAN.checkReceive())            // check if data coming
    {
        CAN.readMsgBuf(&len, buf);    // read data,  len: data length, buf: data buf
        if(CAN.getCanId()==0x604) {  //ECU
          gear=uint8_t(buf[0]);
        }
    }
  //canPrint();
  current=millis();
  pot_pos = analogRead(A2);  //steering wheel clutch potentiometer
    Serial.print("Gear: ");
  Serial.print(gear);
//  Serial.print("   pot_position: ");
//  Serial.print(pot_pos);
//  Serial.print("  clutch_pos:  ");
//  Serial.println(clutch_pos);
  if (digitalRead(shift_up)==LOW){
        if(millis()-button_vibes_up>vibe_debounce){
          vibes_up=1;
        }
     }else{button_vibes_up=millis();}
     if (digitalRead(shift_down)==LOW){
        if(millis()-button_vibes_down>vibe_debounce){
          vibes_down=1;
        }
   }else{button_vibes_down=millis();}

  
  
  //check if the clutch is pressed
  if(pot_pos<(pot_clutch_MIN+pot_error)) {   //the clutch is not pressed
     clutch.writeMicroseconds(1480);                                                                                                         //why?
//     digitalWrite(led_clutch, LOW);
     if((shift_flag==1) && gear!=0 && (digitalRead(shift_up)==LOW) && vibes_up) { //up shift
           gear++;
           if(gear==2){
              //Serial.println("up");
              digitalWrite(sparkcut, LOW);
              delay(spark_delay);
              digitalWrite(HALFDOWN, LOW);
              delay(FULL);
              digitalWrite(HALFDOWN, HIGH);              
              digitalWrite(sparkcut, HIGH);
            
           }else if(gear <= total_gears)  {    //check if we passed the total number of gears
              //Serial.println("up");
              digitalWrite(sparkcut, LOW);
              delay(spark_delay);
              digitalWrite(UP, LOW);
              delay(FULL);
              digitalWrite(UP, HIGH);              
              digitalWrite(sparkcut, HIGH);
           }
           else {gear=5;}
           shift_flag=0;
           previous=millis();
           previous +=interval;
           vibes_up=0;
      }
      if(shift_flag==1 && (digitalRead(shift_down)==LOW) && gear!=0 && vibes_down) {
          gear--;
          if(gear>=1) {    
             clutch.writeMicroseconds(1000);
             digitalWrite(sparkcut, LOW);
             delay(clutch_t);
              digitalWrite(DOWN, LOW);
              delay(FULL);
              digitalWrite(sparkcut, HIGH);
              digitalWrite(DOWN, HIGH);
              clutch.writeMicroseconds(1480);
                   
          }
          else {gear=1;}
          shift_flag=0;
          previous=millis();
          previous +=interval;
          vibes_down=0;
        }
  
  }
  else if(pot_pos>pot_clutch_MIN && pot_pos<pot_clutch_MAX+pot_error){ //the clutch is pressed
    //move servo
    clutch_pos = supermap(pot_pos, pot_clutch_MIN, pot_clutch_MAX, 1600, 1000);
    clutch.writeMicroseconds(clutch_pos);
   
    if((digitalRead(shift_up)==LOW) && shift_flag==1 && vibes_up){      
        gear++;
        if(gear==1) {
            Serial.println("up");
            clutch.writeMicroseconds(1200);
            delay(clutch_t);
              digitalWrite(HALFDOWN, LOW);
              delay(FULL);
              digitalWrite(HALFDOWN, HIGH);
              clutch.writeMicroseconds(clutch_pos);
        }
        else if(gear <= total_gears)  {
            clutch.writeMicroseconds(1200);
            delay(clutch_t);
              digitalWrite(UP, LOW);
              delay(FULL);
              digitalWrite(UP, HIGH);
              clutch.writeMicroseconds(clutch_pos);
        }
        else{gear=5;}
        shift_flag=0;
        previous=millis();
        previous +=interval;
        vibes_up=0;
    }
    if((digitalRead(shift_down)==LOW) && shift_flag==1  && vibes_down){        
        gear--;
        if(gear>0) {
           clutch.writeMicroseconds(1200);
           delay(clutch_t);
              digitalWrite(DOWN, LOW);
              delay(FULL);
              digitalWrite(DOWN, HIGH);
              clutch.writeMicroseconds(clutch_pos);
        }
        else if(gear==0) {
          clutch.writeMicroseconds(1200);
           delay(clutch_t);
              digitalWrite(HALFUP, LOW);
              delay(HALF);
              digitalWrite(HALFUP, HIGH);          
              clutch.writeMicroseconds(clutch_pos);
        }
        else{gear=0;}
        shift_flag=0;
        previous=millis();
        previous +=interval;
        vibes_down=0;
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
  uint8_t n=1;
  clutch_pos=servo_max+(servo_min-servo_max)*(pow((pot_clutch_min/pot_pos),n)-1)/(pow((pot_clutch_min/pot_clutch_max),n)-1);
  return clutch_pos;
}

void canReads() {
  //Serial.println("interrupm");
  CAN.readMsgBuf(&len, buf);
  if(CAN.getCanId()==1532) {       //rear right module
    rr=uint8_t(buf[0]);
  }
  else if(CAN.getCanId()==0x5fd) {  //rear left module
    rl=uint8_t(buf[0]);
    
  }
  else if(CAN.getCanId()==0x5fe) {  //front right module
    fr=uint8_t(buf[0]);
  }
  else if(CAN.getCanId()==0x600) {  //ECU
    rpm=uint16_t(buf[0]<<8 + buf[1]);
    tps=uint8_t(buf[2])/2;                          //prosoxi borei na einai lathos
  }
  else if(CAN.getCanId()==0x604) {  //ECU
    gear=uint8_t(buf[0]);
  }

  else if(CAN.getCanId()==0x666) { //steering wheel
    if(buf[6]&0b00000001) {
      launch=1;
    }
    else{
      launch=0;
      launch_prev=0;
    }
    if(buf[6]&0b00000010) {
      autoshift=1;
    }
    else {
      autoshift=0;
    }
    if(buf[6]&0b00000100){
      neutral=1;
    }
    else {
      neutral=0;                                                      //check
      neutral_prev=0;
    } 
   }
}


void canPrint() {
  Serial.print("launch: ");
  Serial.print(launch);
  Serial.print(" - launch_prev: ");
  Serial.print(launch_prev);
  Serial.print(" - autoshift: ");
  Serial.print(autoshift);
  Serial.print(" - neutral: ");
  Serial.print(neutral);
  Serial.print(" - neutral_prev: ");
  Serial.print(neutral_prev);
  Serial.print(" -gear: ");
  Serial.print(gear);
  Serial.print(" - TPS: ");
  Serial.print(tps);
  Serial.print(" - RPM: ");
  Serial.print(rpm);
  Serial.print(" - RearRightHall: ");
  Serial.print(rr);
  Serial.print(" - RearLeftHall: ");
  Serial.print(rl);
  Serial.print(" - FrontRightHall: ");
  Serial.print(fr);
  Serial.print(" - FrontLeftHall: ");
  Serial.println(fl);
}

/*
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
*/

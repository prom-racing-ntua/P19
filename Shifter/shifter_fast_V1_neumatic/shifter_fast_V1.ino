//Prom racing
//shifter 2019

//GENERAL COMENTS
//o elegxos pou ginetai gia to autoshift mesa sto if tou downshift eisagei megalo delay!! thelei kati pio eksipno..isos mia sinartisi!
//polles allages stis times tou milou
//allagi se kapoioa simeia pou den xreiazetai anapodo downshift logo kainourgiou shifter motor
//canbus den ksero an einai sosto to data aquisition kai to ti morfi mas dinei i ecu
//peirama gia to launch sequence!!


#include <SPI.h>
#include "mcp_can.h"
#include <Servo.h> 

#define pot_clutch_MIN 206   
#define pot_clutch_MAX 390
#define pot_error 15
#define debounceDelay 30
#define spark_delay=10

#define shift_t 100 //milliseconds to keep valve ON on a full shift          //NEEDS FIX becase of motor instead of neumatic valve
#define clutch_t 100 ///wait the servo!

#define auto_shift_up 1
#define sparkcut  2 //Gearcut pin at ECU                                     //FIX PIN because of can shield
#define shift_down 3
#define shift_up 4
#define port1 5  //moves lever up (upshift)
#define port2 6  //moves lever down (downshift)
#define clutch_pin 7  //servo pin
#define total_gears 5

unsigned long up_DebounceTime=0, down_DebounceTime=0;
int gear=0, current_gear_pot=0;
uint16_t pot_pos, clutch_pos, prev_pot_pos=0;
uint8_t shift_up_unpressed, shift_down_unpressed;
unsigned long int prev_time;
//uint8_t gearbox[total_gears+1] = {43,0,143,400,680,920};                   //den xreiazetai

//CANBUS variables
int launch=0, autoshift=0, neutral=0, rpm=0, tps=0
unsigned char len = 0;
unsigned char buf[8];

//autoshift variables
int n2[total_gears]={9500, 9500, 9500, 9500, 9999999};
int n_accel[total_gears]={0, 2500, 3000, 3500, 4800};
int n_brake[total_gears]={0, 3000, 3600, 4500, 5600};
int tms_min=5, tps_max=90; //pososto petaloudas !!!                             prosoxi prepei na doume se ti morfi to dinei i ecu!!!


//launch control variables
int launch_cancel=0;

const int SPI_CS_PIN = 10;                                                      //FIX
MCP_CAN CAN(SPI_CS_PIN);
Servo clutch;

void setup() {
  Serial.begin(115200);
  CAN.begin(CAN_1000KBPS);                                                      //1Mbps
  DDRD = B01100100;
  PORTD = B00011000;
  
  attachInterrupt(0, canReads, FALLING); // start interrupt                    !!porsoxi borei na thelei allagi to 0!!
  
  CAN.init_Mask(0, 0, 0x3ff);                          // there are 2 mask in mcp2515, you need to set both of them
  CAN.init_Mask(1, 0, 0x3ff);                          //!!logika thelei allagi to mask!!
    
  CAN.init_Filt(0, 0, 0x334);                          // front left hall
  CAN.init_Filt(1, 0, 0x335);                          // front right hall
  CAN.init_Filt(2, 0, 0x06);                           // rear hall (right)
  CAN.init_Filt(3, 0, 0x07);                           // launch button + neutral button + autoshift button
  CAN.init_Filt(4, 0, 0x08);                           // ecu rpm & tps
  CAN.init_Filt(5, 0, 0x09);                           // 
 
  clutch.attach(clutch_pin, 1000, 1600);  //1000->1600ms = 0->60 degrees      FIX
  clutch.writeMicroseconds(1000); //initialize servo's position               FIX


void loop() {
  current_gear_pot=analogRead(A1);                                            //FIX VALUES
  if(current_gear_pot<15) {
    gear=0;
  }
  else if(current_gear_pot<80) {
    gear=1;
  }
  else if(current_gear_pot<270) {  ;
    gear=2;
  }
  else if(current_gear_pot<550) {
    gear=3;
  }
  else if(current_gear_pot<800) {
    gear=4;
  }
  else {
    gear=5;
  }  
  pot_pos = analogRead(A0);
  //check if the clutch is pressed
  if(pot_pos<(pot_clutch_MIN-pot_error)) {   //the clutch is not pressed
     clutch.writeMicroseconds(1480);
     if (millis() > up_DebounceTime) { // Debouncing Technique
      if(digitalRead(shift_up)==LOW || (autoshift==1 && rpm>n2[gear])) shift_up_unpressed=true;   //up shift
      else{
        delay(debounceDelay);
        if(shift_up_unpressed==true && (digitalRead(shift_up)==HIGH || (autoshift==1 && rpm>=n2[gear]))){      
           gear++;
           if(gear <= total_gears)  {    //check if we passed the total number of gears
              PORTD |= (1<<5);
              delay(spark_delay);
              PORTD |= (1<<2);
              delay(70);
              PORTD &= ~(1<<2);
              delay(50);
              PORTD &= ~(1<<5);
                           
           }
           else gear=5;
             up_DebounceTime = millis();
             up_DebounceTime += debounceDelay;
             shift_up_unpressed=false; 
        }
      }
   }
  
  if (millis() > down_DebounceTime) { // Debouncing Technique
     if(digitalRead(shift_down)==LOW || autoshift==1) shift_down_unpressed=true;
     else{
        delay(debounceDelay);
        if(shift_down_unpressed==true && (digitalRead(shift_down)==HIGH || ((autoshift==1 && rpm<n2[gear] && tps<=tps_min) && (rpm<=n_brake[gear] || (tps>=tps_max && n<=n_accel[gear]))))){
          gear--;
          if(gear>=1) {    
             clutch.writeMicroseconds(1200);
             delay(clutch_t);
             PORTD |= (1<<6);
             delay(shift_t);
             clutch.writeMicroseconds(1480);             // giati anapoda????????????????????????
             PORTD &= ~(1<<6);      
          }
          else gear=0;
          down_DebounceTime = millis();
          down_DebounceTime += debounceDelay;
          shift_down_unpressed=false; 
        }
      }
    }
  }
  else if(pot_pos>pot_clutch_MIN && pot_pos<pot_clutch_MAX){ //the clutch is pressed

    //move servo
    clutch_pos = supermap(pot_pos, pot_clutch_MIN, pot_clutch_MAX, 1480, 1200);
    clutch.writeMicroseconds(clutch_pos);
    
    if (millis() > up_DebounceTime) { // Debouncing Technique
      if(digitalRead(shift_up)==LOW) shift_up_unpressed=true; 
          else{
            delay(debounceDelay);
            if(shift_up_unpressed==true && digitalRead(shift_up)==HIGH){      
              gear++;
              if(gear <= total_gears)  {
                 clutch.writeMicroseconds(1200);
                 delay(clutch_t);
                 PORTD |= (1<<5);
                 delay(shift_t);
                 PORTD &= ~(1<<5);
                 clutch.writeMicroseconds(clutch_pos);
               }
               else{gear=5;}
               up_DebounceTime = millis();
               up_DebounceTime += debounceDelay;
               shift_up_unpressed=false; 
             }
          }
      }
        
    if (millis() > down_DebounceTime) { // Debouncing Technique
      if(digitalRead(shift_down)==LOW) shift_down_unpressed=true;
      else{
        delay(debounceDelay);
        if(shift_down_unpressed==true && digitalRead(shift_down)==HIGH){        
          gear--;
          if(gear>=1) {
                 clutch.writeMicroseconds(1200);
                 delay(clutch_t);
                 PORTD |= (1<<6);
                 delay(shift_t);
                 PORTD &= ~(1<<6);
                 clutch.writeMicroseconds(clutch_pos);
         }
         else{gear=0;}
         down_DebounceTime = millis();
         down_DebounceTime +=debounceDelay;
         shift_down_unpressed=false;
       }
     }
   }
   if(launch==1) {
      clutch.writeMicroseconds(1200);                              //shift up to be ready for the lsunch
      delay(clutch_t);                                             //tha xreiastei na bei deutera??
      PORTD |= (1<<5);
      delay(shift_t);
      PORTD &= ~(1<<5);
      clutch.writeMicroseconds(clutch_pos);
      pot_pos = analogRead(A0);
      //LAUNCH SEQUENCE
      while(1){                    
            if(pot_pos<(pot_clutch_MIN-pot_error) { //clutch not presed but launch button is still presed
                if(launch==0) break;                //launch button is released!!
           }
           else {                                   //clutch is presed && launch button is presed
              if(launch==0){ 
                 launch_cancel=1;                   //check if launch button is released before fully releasing the clutch!!! that means that we cancel the launch control!!!!!!!!!!
                 break;
              }
           }
           pot_pos = analogRead(A0);             //check clutch position
      }
      while(pot_pos<(pot_clutch_MIN-pot_error && lauch_cancel==0){   //clutch is not pressed && launch has not been canceled //na boun kai alles sinthikes gia asfaleia!!!!!!!!!!!!!!!!!!!
        pot_pos = analogRead(A0);              //check clutch position             pooooli argooo!! thelei allo tropo elegxou
        //launch code!
      
      
      }
      launch=0;
      launch_cancel=0;                                  
   }
   if(neutral==1) {
      clutch.writeMicroseconds(1200);
      delay(clutch_t);
      for(int i=0; i<gear; i++) {                  //shift down all the way to neutral
      PORTD |= (1<<6);
      delay(shift_t);                                             //ISOS THELEI MEGALITERO DELAY
      PORTD &= ~(1<<6); 
      }
      clutch.writeMicroseconds(1480);
      gear=0;
      neutral=0;
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


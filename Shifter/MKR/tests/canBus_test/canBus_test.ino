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

#include <SPI.h>
#include "mcp_can.h"

//CANBUS variables
volatile uint8_t launch=0, autoshift=0, neutral=0;
volatile uint8_t launch_prev=0, neutral_prev=0;
unsigned char len = 0;
unsigned char buf[8];
volatile uint8_t gear=0, tps=0, rr=0, rl=0, fr=0, fl=0;
volatile uint16_t rpm=0;

const int SPI_CS_PIN = 3;
MCP_CAN CAN(SPI_CS_PIN);

void setup() {
  Serial.begin(115200);
  CAN.begin(CAN_500KBPS);                           // 1Mbps
 attachInterrupt(7, canReads, FALLING);               // CAN BUS interrupt
  
  CAN.init_Mask(0, 0, 0x000);                          // there are 2 mask in mcp2515, you need to set both of them
  CAN.init_Mask(1, 0, 0xfff);                          // !!logika thelei allagi to mask!!
    
  CAN.init_Filt(0, 0, 0x5fc);                          // rear right hall
  CAN.init_Filt(1, 0, 0x5fd);                          // rear left hall
  CAN.init_Filt(2, 0, 0x5fe);                          // front right hall
  CAN.init_Filt(3, 0, 0x600);                          // ecu rpm &tps
  CAN.init_Filt(4, 0, 0x604);                          // ecu gear
  CAN.init_Filt(5, 0, 0x666);                          // launch button + neutral button + autoshift button
}
  
void loop() {
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
  delay(500);
  
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

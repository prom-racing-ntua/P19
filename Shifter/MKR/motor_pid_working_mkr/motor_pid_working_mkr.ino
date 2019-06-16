//Prom racing
//shifter 2019

/*              :AREF      5V: 
 *              :DAC      VIN:
 *    AUX3      :A1      3.3V:
 * CLUTCH       :        GND:
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


#include <PID_v1.h>
#define CHA      5                      // Quadrature encoder A pin
#define CHB      6                       // Quadrature encoder B pin
#define M1              0                       // PWM outputs to L298N H-Bridge motor driver module
#define M2              1
#define button          A3
#include <Servo.h> 
Servo clutch;
double kp = 40 , ki = 2.3 , kd = 0.01;             // modify for optimal performance
double input = 0, output = 0, setpoint = 0;
long temp;
volatile long encoderPos = 0;
unsigned long current, previous, interval = 150;
unsigned char CHAprev = 1;
PID myPID(&input, &output, &setpoint, kp, ki, kd, DIRECT);  // if motor will only run at full speed try 'REVERSE' instead of 'DIRECT'

#define clutch_pin  10      //servo signal
void setup() {
  //setPWMfrequency(); 
  pinMode(CHA, INPUT_PULLUP);                  // quadrature encoder input A
  pinMode(CHB, INPUT_PULLUP);                  // quadrature encoder input B
  pinMode(button, INPUT_PULLUP);
  //TCCR1B = TCCR1B & 0b11111000 | 1;                   // set 31KHz PWM to prevent motor noise
  myPID.SetMode(AUTOMATIC);
  myPID.SetSampleTime(10);
  myPID.SetOutputLimits(-255, 255);
  Serial.begin (115200);                              // for debugging
  setpoint = 0;                       // modify to fit motor and encoder characteristics, potmeter connected to A0
  
  clutch.attach(clutch_pin, 1000, 1600);
  }

void loop() {
//  input = encoderPos ;                                // data from encoder
//  Serial.println(encoderPos);                      // monitor motor position
//  myPID.Compute();                                    // calculate new output
//  pwmOut(output);
   clutch.writeMicroseconds(1500);                      // initialize servo's position               FIX
 
  Serial.print("  -  ");
  Serial.print(output);// drive L298N H-Bridge module
  Serial.print("  -  ");
  Serial.println(setpoint);// drive L298N H-Bridge module
  // if((output<=1.5 )&& (output>=-1.7)) {
  //  setpoint=0;
  // }
  Serial.println(encoderPos);
  if (digitalRead(button) == LOW) {
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


void shiftup() {                      //FIX

    
  setpoint = 12;
  previous = millis();
  previous += interval;
  // while((output<=1.7 )&& (output>=-1.7)){

  while (1) {
    current = millis();
    if (current > previous) {
      
      break;
    }
    mouni();
    input = encoderPos ;                                // data from encoder
    myPID.Compute();                                    // calculate new output
    pwmOut(output);
  }
  setpoint = 0;
  previous = millis();
  previous += interval;
  //while((output<=1.7 )&& (output>=-1.7)){
  while (1) {
    current = millis();
    if (current > previous) {    
      break;
    }
    mouni();
    input = encoderPos ;                                // data from encoder

    myPID.Compute();                                    // calculate new output
    pwmOut(output);
  }
    output=0;
  analogWrite(M1, 0);
  analogWrite(M2, 0);
  interrupts();
}
void mouni(){
  if ((digitalRead(CHA)==LOW) && CHAprev){
      CHAprev=0;
      if(digitalRead(CHB)==HIGH){
        encoderPos--;
        }else{
        encoderPos++;
      }
  }
  if (digitalRead(CHA)==HIGH){CHAprev=1;}
}

void setPWMfrequency() { 
  REG_GCLK_GENDIV = GCLK_GENDIV_DIV(255) |          // Divide the 48MHz clock source by divisor 255: 48MHz/255= 188235.2941176 Hz
                    GCLK_GENDIV_ID(4);            // Select Generic Clock (GCLK) 4
  while (GCLK->STATUS.bit.SYNCBUSY);              // Wait for synchronization

  REG_GCLK_GENCTRL = GCLK_GENCTRL_IDC |           // Set the duty cycle to 50/50 HIGH/LOW
                     GCLK_GENCTRL_GENEN |         // Enable GCLK4
                     GCLK_GENCTRL_SRC_DFLL48M |   // Set the 48MHz clock source
                     GCLK_GENCTRL_ID(4);          // Select GCLK4
  while (GCLK->STATUS.bit.SYNCBUSY);              // Wait for synchronization

  // Enable the port multiplexer for the digital pin D0 
  PORT->Group[g_APinDescription[2].ulPort].PINCFG[g_APinDescription[2].ulPin].bit.PMUXEN = 1;
  
  // Connect the TCC0 timer to digital output D0 - port pins are paired odd PMUO and even PMUXE
  // F & E specify the timers: TCC0, TCC1 and TCC2
  PORT->Group[g_APinDescription[2].ulPort].PMUX[g_APinDescription[2].ulPin >> 1].reg = PORT_PMUX_PMUXO_F;

  // Feed GCLK4 to TCC0 and TCC1
  REG_GCLK_CLKCTRL = GCLK_CLKCTRL_CLKEN |         // Enable GCLK4 to TCC0 and TCC1
                     GCLK_CLKCTRL_GEN_GCLK4 |     // Select GCLK4
                     GCLK_CLKCTRL_ID_TCC0_TCC1;   // Feed GCLK4 to TCC0 and TCC1             //FIX
  while (GCLK->STATUS.bit.SYNCBUSY);              // Wait for synchronization

  // Dual slope PWM operation: timers countinuously count up to PER register value then down 0
  REG_TCC1_WAVE |= TCC_WAVE_POL(0xF) |         // Reverse the output polarity on all TCC0 outputs
                    TCC_WAVE_WAVEGEN_DSBOTH;    // Setup dual slope PWM on TCC0
  while (TCC1->SYNCBUSY.bit.WAVE);               // Wait for synchronization

  // Each timer counts up to a maximum or TOP value set by the PER register,
  // this determines the frequency of the PWM operation: 
  REG_TCC0_PER = 3;         // Set the frequency of the PWM on TCC0 to 31kHz
  while (TCC1->SYNCBUSY.bit.PER);                // Wait for synchronization
  
  // Set the PWM signal to output 50% duty cycle
  REG_TCC1_CC0 = 1.5;         // TCC0 CC0 - on D0  //or 3 for 100%duty cycle
  while (TCC1->SYNCBUSY.bit.CC0);                // Wait for synchronization
  
  // Divide the 48MHz signal by 1 giving 48MHz (20.83ns) TCC0 timer tick and enable the outputs
  REG_TCC1_CTRLA |= TCC_CTRLA_PRESCALER_DIV1 |    // Divide GCLK4 by 1
                    TCC_CTRLA_ENABLE;             // Enable the TCC0 output
  while (TCC1->SYNCBUSY.bit.ENABLE);              // Wait for synchronization
}

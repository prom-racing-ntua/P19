//Launch_control
//P19

#include<Servo.h>

#define R
#define J_w //moment of inertia_wheel
#define m //mass
#define K //rate of convergence
#define Tmax_engine
#define CP_max //clutch position
#define CP_min
float omegr=0,omegr_r=0,omegr_l=0;
float vel_f=0; // velocity of front wheels
float d_sr[5]={1,2,3,4,5}; //desired slip ratio
float z,c1,c2,T,CP;
float c_s; //tan of diagram (Fx,s)

void setup(){
  float c1=(CP_max-CP_min)/Tmax_engine;
  float c2=J_w/R(R^2*c_s/J_w+(1+d_sr[--])*c_s/m);
}


void loop(){
  omegr_r=analogRead(--);
  omegr_l=analogRead(--);
  omegr=(omegr_r+omegr_l)/2;
  vel_f=analogRead(--);
  z=R*omegr-(1+d_sr[--])*vel_f;
  T=c2*(omegr*R/vel_f-1)-K*z;
  CP=CP_max+c1*T;
}

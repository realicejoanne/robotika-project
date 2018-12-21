#include <NewPing.h>

#define rightMotor_Dir 4  // arah putar (Motor 1 / kanan)
#define rightMotor_Vel 5  // kontrol kecepatan (Motor 1 / Kiri)
#define leftMotor_Vel 6
#define leftMotor_Dir 7
#define fullspeed 255
#define nospeed 0

int tengah;
int kiri;
int kanan;

int serialData;
int pinLED = 13;

void mundur(){
  digitalWrite(rightMotor_Dir,HIGH);   
  analogWrite(rightMotor_Vel,200);  
  digitalWrite(leftMotor_Dir,HIGH); 
  analogWrite(leftMotor_Vel,200);  
}
void maju(){
   digitalWrite(rightMotor_Dir,LOW); 
   analogWrite(rightMotor_Vel,150);  
   digitalWrite(leftMotor_Dir,LOW);  
   analogWrite(leftMotor_Vel,150);  
}
void berhenti(){
   digitalWrite(rightMotor_Dir,LOW);  
   analogWrite(rightMotor_Vel,nospeed);  
   digitalWrite(leftMotor_Dir,LOW);  
   analogWrite(leftMotor_Vel,nospeed);  
}
void belokkiri(){
   digitalWrite(leftMotor_Dir,HIGH);  
   analogWrite(leftMotor_Vel,160);  
   digitalWrite(rightMotor_Dir,LOW);  
   analogWrite(rightMotor_Vel,140);  
   //delay(200); 
}
void belokkanan(){
   digitalWrite(rightMotor_Dir,HIGH);  
   analogWrite(rightMotor_Vel,150);  
   digitalWrite(leftMotor_Dir,LOW);  
   analogWrite(leftMotor_Vel,130);  
   //delay(200);
}

void setup(){
  pinMode (4,OUTPUT);  
  pinMode (5,OUTPUT);  
  pinMode (6,OUTPUT);  
  pinMode (7,OUTPUT);  
  pinMode (pinLED, OUTPUT);
  
  Serial.begin(9600);
}
void loop(){
  //READ DATA FROM SERIAL FROM PYTHON
  if(Serial.available() > 0){
    serialData = Serial.read();
    Serial.print(serialData);

    if(serialData == '1'){
      belokkanan();
      digitalWrite(pinLED, HIGH);
    } 
    else if(serialData == '2'){
      belokkiri();
      digitalWrite(pinLED, HIGH);
    }  
    else if (serialData == '3'){
      maju();
      digitalWrite(pinLED, HIGH);
    }
  }
}

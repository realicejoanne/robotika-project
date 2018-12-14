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

#define TRIGGER_PIN 19
#define ECHO_PIN 18
#define MAX_DISTANCE 500
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

#define TRIGGER_PIN1 17
#define ECHO_PIN1 16
NewPing sonar1(TRIGGER_PIN1, ECHO_PIN1, MAX_DISTANCE);

#define TRIGGER_PIN2 15
#define ECHO_PIN2 14
NewPing sonar2(TRIGGER_PIN2, ECHO_PIN2, MAX_DISTANCE);

void mundur(){
  digitalWrite(rightMotor_Dir,HIGH);   
  analogWrite(rightMotor_Vel,200);  
  digitalWrite(leftMotor_Dir,HIGH); 
  analogWrite(leftMotor_Vel,200);  
}
void maju(){
   digitalWrite(rightMotor_Dir,LOW); 
   analogWrite(rightMotor_Vel,200);  
   digitalWrite(leftMotor_Dir,LOW);  
   analogWrite(leftMotor_Vel,200);  
}
void berhenti(){
   digitalWrite(rightMotor_Dir,LOW);  
   analogWrite(rightMotor_Vel,nospeed);  
   digitalWrite(leftMotor_Dir,LOW);  
   analogWrite(leftMotor_Vel,nospeed);  
}
void belokkiri(){
   digitalWrite(leftMotor_Dir,HIGH);  
   analogWrite(leftMotor_Vel,200);  
   digitalWrite(rightMotor_Dir,LOW);  
   analogWrite(rightMotor_Vel,150);  
   //delay(200); 
}
void belokkanan(){
   digitalWrite(rightMotor_Dir,HIGH);  
   analogWrite(rightMotor_Vel,200);  
   digitalWrite(leftMotor_Dir,LOW);  
   analogWrite(leftMotor_Vel,150);  
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
    /*else if(serialData == '0'){
      berhenti();
      digitalWrite(pinLED, LOW);
    }*/
  }
}

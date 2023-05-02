#include <SoftwareSerial.h>
#include <Servo.h>

SoftwareSerial btSerial(2, 3);
Servo servo;

void setup(){
  Serial.begin(9600);
  btSerial.begin(9600);
  servo.attach(8);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
}

char data;
char record = '2';
char engine = '4';
int steer = 65;
int steer_prev;

void forward(int vel){
  digitalWrite(11, HIGH);
  digitalWrite(12, LOW);
  analogWrite(A0, vel);
}

void backward(int vel){
  digitalWrite(11, LOW);
  digitalWrite(12, HIGH);
  analogWrite(A0, vel);
}

void loop(){
  if(btSerial.available()){
    data = btSerial.read();
  }

  if(data == '1' or data == '2'){
    record = data;
    Serial.write(data);
  }else if(data == '3' or data == '4'){
    engine = data;
  }

  if(data == 'a'){
    steer = 5;
  }else if(data == 'b'){
    steer = 15;
  }else if(data == 'c'){
    steer = 25;
  }else if(data == 'd'){
    steer = 35;
  }else if(data == 'e'){
    steer = 45;
  }else if(data == 'f'){
    steer = 55;
  }else if(data == 'g'){
    steer = 65;
  }else if(data == 'h'){
    steer = 75;
  }else if(data == 'i'){
    steer = 85;
  }else if(data == 'j'){
    steer = 95;
  }

  if(steer_prev != steer){
    servo.write(steer);
    steer_prev = steer;
  }

  if(data == 'A'){
    backward(250);
  }else if(data == 'B'){
    backward(200);
  }else if(data == 'C'){
    backward(150);
  }else if(data == 'D'){
    backward(0);
  }else if(data == 'E'){
    forward(100);
  }else if(data == 'F'){
    forward(150);
  }else if(data == 'G'){
    forward(200);
  }else if(data == 'H'){
    forward(250);
  }
}

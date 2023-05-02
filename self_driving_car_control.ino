#include <SoftwareSerial.h>

SoftwareSerial btSerial(2, 3);

#define greenLED 5
#define redLED 6
#define RightButton 7
#define LeftButton 8
#define rightLever A0
#define leftLever A1

int RightButtonMode = 0;
int LeftButtonMode = 0;
char steer_sign = 'f';
char velocity_sign;
char steer_sign_prev = 'f';
char velocity_sign_prev;

char temp_steers[3];
char temp_velocities[3];

int RightButtonValue;
int LeftButtonValue;
int potention_right;
int potention_right_prev;
int potention_left;
int potention_left_prev;
int steer;
int velocity;

void setup(){
  Serial.begin(9600);
  btSerial.begin(9600);
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(LeftButton, INPUT);
  pinMode(RightButton, INPUT);
}

void loop(){
  RightButtonValue = digitalRead(RightButton);
  LeftButtonValue = digitalRead(LeftButton);

  for(int i=0; i<3; i++){
    potention_right = analogRead(rightLever);
    potention_right = potention_right - 250;
    steer = map(potention_right, 0, 500, 0, 120);
  
    if(0<steer && steer<15){
      temp_steers[i] = 'a';
    }else if(25<=steer && steer<30){
      temp_steers[i] = 'b';
    }else if(35<=steer && steer<40){
      temp_steers[i] = 'c';
    }else if(45<=steer && steer<50){
      temp_steers[i] = 'd';
    }else if(55<=steer && steer<60){
      temp_steers[i] = 'e';
    }else if(65<=steer && steer<70){
      temp_steers[i] = 'f';
    }else if(75<=steer && steer<80){
      temp_steers[i] = 'g';
    }else if(85<=steer && steer<90){
      temp_steers[i] = 'h';
    }else if(95<=steer && steer<100){
      temp_steers[i] = 'i';
    }else if(105<=steer){
      temp_steers[i] = 'j';
    }
  }

  if(temp_steers[0] == temp_steers[1] && temp_steers[1] == temp_steers[2]){
    steer_sign = temp_steers[0];
  }
  
  if(steer_sign_prev != steer_sign){
    btSerial.write(steer_sign);
    steer_sign_prev = steer_sign;
  }

  for(int i=0; i<3; i++){
    potention_left = analogRead(leftLever);
    potention_left = potention_left - 250;
    velocity = map(potention_left, 0, 500, 0, 90);
  
    if(0<velocity && velocity<10){
      temp_velocities[i] = 'A';
    }else if(15<velocity && velocity<20){
      temp_velocities[i] = 'B';
    }else if(25<velocity && velocity<30){
      temp_velocities[i] = 'C';
    }else if(35<velocity && velocity<40){
      temp_velocities[i] = 'D';
    }else if(45<velocity && velocity<50){
      temp_velocities[i] = 'E';
    }else if(55<velocity && velocity<60){
      temp_velocities[i] = 'F';
    }else if(65<velocity && velocity<70){
      temp_velocities[i] = 'G';
    }else if(80<velocity){
      temp_velocities[i] = 'H';
    }
  }

  if(temp_velocities[0] == temp_velocities[1] && temp_velocities[1] == temp_velocities[2]){
    velocity_sign = temp_velocities[0];
  }
  
  if(velocity_sign_prev != velocity_sign){
    btSerial.write(velocity_sign);
    velocity_sign_prev = velocity_sign;
    Serial.println(velocity_sign);
  }

  if(RightButtonValue == HIGH){
    delay(200);
    if(RightButtonMode == 0){
      RightButtonMode = 1;
      btSerial.write('1');  //Camera on
    }else{
      RightButtonMode = 0;
      btSerial.write('2');  //camera off
    }
  }

  if(LeftButtonValue == HIGH){
    delay(200);
    if(LeftButtonMode == 0){
      LeftButtonMode = 1;
      btSerial.write('3');  //Power on
    }else{
      LeftButtonMode = 0;
      btSerial.write('4');  //power off
    }
  }

  if(RightButtonMode == 1){
    digitalWrite(greenLED, HIGH);
  }else{
    digitalWrite(greenLED, LOW);
  }

  if(LeftButtonMode == 1){
    digitalWrite(redLED, HIGH);
  }else{
    digitalWrite(redLED, LOW);
  }
}

#include <Servo.h>

Servo theta1;
Servo theta2;
Servo theta3;
Servo gripper;

#define PIN1 11
#define PIN2 9
#define PIN3 10
#define PIN4 6

int actualPosition[3] = {0,0,0};

void moveToAngle(int angle1, int actualPos1, int angle2, int actualPos2, int angle3, int actualPos3){
  slowMoves(theta1,angle1, actualPos1);
  delay(250);
  slowMoves(theta2,angle2, actualPos2);
  delay(250);
  slowMoves(theta3,angle3, actualPos3);
}

void slowMoves(Servo servomotor, int angle, int currentPosition){
  if (currentPosition < angle){
    // faire tourner dans le sens +
   while(currentPosition <= angle){
      currentPosition ++;
      servomotor.write(currentPosition);
      delay(20);
      Serial.println(currentPosition);
   } 
  }
  else 
  {
    // faire tourner dans le sens -
    while(currentPosition > angle){
      currentPosition --;
      servomotor.write(currentPosition);
      delay(20);
      Serial.println(currentPosition);
   }
  }
}

void openGripper(){
  gripper.write(90);
}

void closeGripper(){
  gripper.write(0);
}

void setUpServo()
{
  theta1.attach(PIN1);
  theta2.attach(PIN2);
  theta3.attach(PIN3);
  gripper.attach(PIN4);
  theta1.write(0);
  theta2.write(0);
  theta3.write(0);
  gripper.write(0);
}

void updateAngle(int newPos1, int newPos2, int newPos3){
  actualPosition[0] = newPos1;
  actualPosition[1] = newPos2;
  actualPosition[2] = newPos3;
}

void setup()
{
  Serial.begin(9600);
  setUpServo();
}

void loop(){
  moveToAngle(30,0,30,0,30,0);
  closeGripper();
  updateAngle(30,30,30);
  delay(3000);

  moveToAngle(0,30, 0, 30, 0, 30);
  openGripper();
  updateAngle(0,0,0);
  delay(3000);
}
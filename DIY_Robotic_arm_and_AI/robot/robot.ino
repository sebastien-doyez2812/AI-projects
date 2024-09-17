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
int numbers[3];

void moveToAngle(int angle1, int actualPos1, int angle2, int actualPos2, int angle3, int actualPos3){
  slowMoves(theta1,angle1, actualPos1);
  delay(2000);
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
  gripper.write(0);
}

void closeGripper(){
  gripper.write(90);
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
  gripper.write(90);
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


void loop() {
  if (Serial.available() > 0) {
    String str_data = Serial.readStringUntil('\n'); 

    str_data.trim();

    int startIndex = str_data.indexOf('[') + 1;
    int endIndex = str_data.indexOf(']');

    if (startIndex > 0 && endIndex > startIndex) {
      String numbersString = str_data.substring(startIndex, endIndex);
      
      int numberCount = 0;
      int commaIndex = 0;
      int previousCommaIndex = 0;

      while ((commaIndex = numbersString.indexOf(',', previousCommaIndex)) != -1 && numberCount < 3) {
        String numberString = numbersString.substring(previousCommaIndex, commaIndex);
        numberString.trim();  
        numbers[numberCount++] = numberString.toInt();  
        previousCommaIndex = commaIndex + 1;
      }

      if (previousCommaIndex < numbersString.length() && numberCount < 3) {
        String numberString = numbersString.substring(previousCommaIndex);
        numberString.trim();  
        numbers[numberCount++] = numberString.toInt();
      }

      int o1 = numbers[0];
      int o2 = numbers[1];
      int o3 = numbers[2];
      for (int i = 0; i < 3; i ++)
      {
        numbers[i] = 0;
      }
      slowMoves(theta1, o1, 0);
      delay(500);
      slowMoves(theta2, o2, 0);
      delay(1000);
      openGripper();
      delay(500);
      slowMoves(theta3, o3, 0);
      delay(500);
      closeGripper();
      delay(500);
      slowMoves(theta3, 0, o3);
      delay(500);
      slowMoves(theta2, 0, o2);
      delay(1000);
      slowMoves(theta3, 0, o3);
      delay(1000);
      openGripper();
    } else {
      Serial.println("Error message");
      Serial.println(str_data);
    }
  }      
}

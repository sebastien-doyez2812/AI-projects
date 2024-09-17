#include <Servo.h>

Servo theta1;
Servo theta2;
Servo theta3;
Servo gripper;

#define PIN1 11
#define PIN2 9
#define PIN3 10
#define PIN4 6

int OK = 1;

int actualPosition[3] = {0,0,0};
int numbers[3];

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
  theta2.write(90);
  theta3.write(90);
  gripper.write(90);
}

void setup()
{
  Serial.begin(9600);
  setUpServo();
}

void moveToTarget(int o1, int o2, int o3)
{
  slowMoves(theta1, o1, 0);
  delay(500);
  openGripper();
  delay(500);
  slowMoves(theta3, o3, 90);  
  delay(500);
  slowMoves(theta2, o2, 90);
  delay(500);
  closeGripper();
  delay(500);
  slowMoves(theta3, 90, o3);
  delay(500);
  slowMoves(theta2, 90, o2);
  delay(500);
  slowMoves(theta1, 130, o1);
  delay(500);
  slowMoves(theta2, o2, 90);
  delay(500);
  slowMoves(theta3, o3, 90);
  openGripper();
  delay(1000);
  slowMoves(theta2, 90, o2 );
  delay(200);
  slowMoves(theta3, 90, o3 );
  closeGripper();
  delay(200);
  slowMoves(theta1, 0, 130);
}

void loop() {
  if (OK == 1 )
  {
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
        moveToTarget(o1,o2,o3);
        OK = 0;
      } else {
        Serial.println("Error message");
        Serial.println(str_data);
      }
    }   
  }
}

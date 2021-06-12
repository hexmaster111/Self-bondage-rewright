#include <Arduino.h>
#include <Servo.h>

int datafromUser = 0;

Servo keyReleaseServo;

void setup()
{
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  keyReleaseServo.attach(2);
}

void inputDesion(int opperation)
{
  switch (opperation)
  {
  case '0': //Hold
    keyReleaseServo.write(180);
    digitalWrite(LED_BUILTIN, LOW);
    break;
  case '1': //Release
    keyReleaseServo.write(0);
    digitalWrite(LED_BUILTIN, HIGH);
    break;
  case '2': //90 deg
    keyReleaseServo.write(90);
    digitalWrite(LED_BUILTIN, HIGH);
    break;
  case '3': //unused

    break;

  default:
    for (int i = 0; i <= 255; i++)
    {
      digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
      // delay(1000);
    }
    break;
  }
}

void loop()
{
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0)
  {
    datafromUser = Serial.read();
  }
  //ima make this a case statement but for now this is good enough for testing
  //@TODO Make this a case statement

  inputDesion(datafromUser);
}
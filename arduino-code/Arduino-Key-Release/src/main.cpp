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

void loop()
{
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0)
  {
    datafromUser = Serial.read();
  }
 //ima make this a case statement but for now this is good enough for testing
 //@TODO Make this a case statement
  if (datafromUser == '1')
  {
    digitalWrite(LED_BUILTIN, HIGH);
    keyReleaseServo.write(0);
  }
  else if (datafromUser == '0')
  {
    digitalWrite(LED_BUILTIN, LOW);
    keyReleaseServo.write(180);
  }
}
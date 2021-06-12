#include <Arduino.h>

int datafromUser = 0;
void setup()
{
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0)
  {
    datafromUser = Serial.read();
  }

  if (datafromUser == '1')
  {
    digitalWrite(LED_BUILTIN, HIGH);
  }
  else if (datafromUser == '0')
  {
    digitalWrite(LED_BUILTIN, LOW);
  }
}
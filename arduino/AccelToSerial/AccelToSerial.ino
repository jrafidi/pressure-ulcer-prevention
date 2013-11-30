int x1, y1, z1, x2, y2, z2, x3, y3, z3;

void setup()
{
  Serial.begin(9600);      // sets the serial port to 9600
}

void loop()
{
  x1 = analogRead(0);       // read analog input pin 0
  y1 = analogRead(1);       // read analog input pin 1
  z1 = analogRead(2);       // read analog input pin 2
  x2 = analogRead(3);       // read analog input pin 3
  y2 = analogRead(4);       // read analog input pin 4
  z2 = analogRead(5);       // read analog input pin 5
  x3 = analogRead(6);       // read analog input pin 6
  y3 = analogRead(7);       // read analog input pin 7
  z3 = analogRead(8);       // read analog input pin 8
  Serial.print("[");
  Serial.print(x1, DEC);    // print the acceleration in the X axis
  Serial.print(",");       // prints a space between the numbers
  Serial.print(y1, DEC);    // print the acceleration in the Y axis
  Serial.print(",");       // prints a space between the numbers
  Serial.print(z1, DEC);  // print the acceleration in the Z axis
  Serial.print(",");       // prints a space between the numbers
  Serial.print(x2, DEC);    // print the acceleration in the X axis
  Serial.print(",");       // prints a space between the numbers
  Serial.print(y2, DEC);    // print the acceleration in the Y axis
  Serial.print(",");       // prints a space between the numbers
  Serial.print(z2, DEC);  // print the acceleration in the Z axis
  Serial.print(",");       // prints a space between the numbers
  Serial.print(x3, DEC);    // print the acceleration in the X axis
  Serial.print(",");       // prints a space between the numbers
  Serial.print(y3, DEC);    // print the acceleration in the Y axis
  Serial.print(",");       // prints a space between the numbers
  Serial.print(z3, DEC);  // print the acceleration in the Z axis
  Serial.println("]");
  delay(1000);              // wait 1s for next reading
}

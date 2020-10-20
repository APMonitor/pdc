// Arduino code tclab.ino
const int pinT1   = 0;
const int pinT2   = 2; 
float mV = 0.0;
float degC = 0.0;
for (int i = 0; i < n; i++) {
  mV = (float) analogRead(pinT1) * (3300.0/1024.0);
  degC = degC + (mV - 500.0)/10.0;
}
degC = degC / float(n);   
Serial.println(degC);
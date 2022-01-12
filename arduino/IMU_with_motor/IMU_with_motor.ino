#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;
sensors_event_t a, g, temp;

// L298N motor driver pins
const int enPin = 3; //need PWM
const int in1 = 4;
const int in2 = 5;

int incomingByte; 

void setup() {
  // setup IMU
  setupIMU();
  
  // setup motor pins
  pinMode(enPin, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  Serial.begin(115200);
}

void setupIMU() {
  // Try to initialize 
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1){ // prevent running more code
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  /*  acceleration can be 2g, 4g, 8g, or 16g 
   *  defaults to 2g
   *  the lower, the more sensitive the readings will be
   */
  mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
  
  /*  acceleration can be 250, 500, 1000, 2000
   *  defaults to 250 degrees per second
   *  the lower, the more sensitive the readings will be
   */
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);

  /*  acceleration can be 260, 184, 94, 44, 21, 10, 5
   *  this sets the cut-off freq of a low pass filter
   *  260Hz disables the filter
   */
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}

void loop() {
  mpu.getEvent(&a, &g, &temp); // get readings from IMU
  displaySerial();
  checkIncoming();
  delay(10); // 100Hz sampling rate
}

void displaySerial() {
  // acceleration units are in m/s^2
  Serial.print(a.acceleration.x);  Serial.print(",");
  Serial.print(a.acceleration.y);  Serial.print(",");
  Serial.print(a.acceleration.z);  Serial.print(",");

  // rotation units are in rad/s
  Serial.print(g.gyro.x);  Serial.print(",");
  Serial.print(g.gyro.y);  Serial.print(",");
  Serial.println(g.gyro.z);
}

void checkIncoming() {
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    // if it's a capital H (ASCII 72), turn on the LED:
    if (incomingByte == 'H') {
      // turn on motor
      motorOn();
    }
    // if it's an L (ASCII 76) turn off the LED:
    if (incomingByte == 'L') {
      // turn off motor
      motorOff();
    }
  }
}

void motorOn() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enPin, 200);
}

void motorOff() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
}

#include <Wire.h>
#include <VL53L0X.h>

VL53L0X sensor;

/*Example sketch to control a stepper motor with A4988/DRV8825 stepper motor driver and Arduino without a library. More info: https://www.makerguides.com */
//MAX_ROTATIONS = 6

// Define stepper motor connections and steps per revolution:
#define dirPinV 2
#define stepPinV 3

#define dirPinR 4
#define stepPinR 5

int verticalSteps = 0;
int horizontalSteps = 0;

void moveVertical() {
  for (int i = 0; i < 200; i++) {
    digitalWrite(stepPinV, HIGH);
    delayMicroseconds(5000);
    digitalWrite(stepPinV, LOW);
    delayMicroseconds(5000);
    verticalSteps++;
  }
}

void rotateObject() {
  digitalWrite(stepPinR, HIGH);
  delayMicroseconds(2000);
  digitalWrite(stepPinR, LOW);
  delayMicroseconds(2000);
  horizontalSteps++;
}

#define stepsPerRevolution 200

void setup() {
  // Declare pins as output:
  pinMode(stepPinV, OUTPUT);
  pinMode(dirPinV, OUTPUT);
  pinMode(stepPinR, OUTPUT);
  pinMode(dirPinR, OUTPUT);

  Serial.begin(9600);

  Wire.begin();
  sensor.setTimeout(0);
  if (!sensor.init())
  {
    Serial.println("-2");
    while (1) {}
  }
  else {
    Serial.println("5");
  }

  sensor.setMeasurementTimingBudget(100000);

  digitalWrite(dirPinV, HIGH);
}

void loop() {
  // Set the spinning direction clockwise:
  while (!Serial.available());
  while (Serial.available()) {
    Serial.read();
  }

  bool done = 0;

  digitalWrite(dirPinV, HIGH);

  while (!done) {
    done = 1;
    horizontalSteps = 0;
    if (verticalSteps > 1800) {
      break;
    }
    for (int i = 0; i < stepsPerRevolution; i++) {
      int measurement = sensor.readRangeSingleMillimeters();
      Serial.println(measurement);
      if (measurement < 8000) {
        done = 0;
        Serial.print("20");
        Serial.println();
        Serial.print(horizontalSteps);
        Serial.print(" ");
        Serial.print(measurement);
        Serial.print(" ");
        Serial.print(verticalSteps);
        Serial.println();
        Serial.read();
        delay(200);
      }
      else if (measurement > 60000) {
        Serial.print("-30");
        Serial.println();
      }
      rotateObject();
    }
    if (!done) {
      moveVertical();
    }
  }

  Serial.println("10");

  digitalWrite(dirPinV, LOW);
  verticalSteps = -verticalSteps;
  while(verticalSteps < 0) {
    moveVertical();
  }

  delay(1000); 
}

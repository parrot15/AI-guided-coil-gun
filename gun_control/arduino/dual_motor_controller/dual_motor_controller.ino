#define MOTOR1    1
#define EN_PIN1   8   // Enable
#define STEP_PIN1 9   // Step
#define DIR_PIN1  10  // Direction

#define MOTOR2    2
#define EN_PIN2   11  // Enable
#define STEP_PIN2 12  // Step
#define DIR_PIN2  13  // Direction

#define STEP_DELAY_US  1000  // Adjust this delay to change speed

void setup() {
  pinMode(EN_PIN1, OUTPUT);
  pinMode(STEP_PIN1, OUTPUT);
  pinMode(DIR_PIN1, OUTPUT);
  digitalWrite(EN_PIN1, LOW);  // Enable the motor
  digitalWrite(DIR_PIN1, HIGH);  // Set direction

  pinMode(EN_PIN2, OUTPUT);
  pinMode(STEP_PIN2, OUTPUT);
  pinMode(DIR_PIN2, OUTPUT);
  digitalWrite(EN_PIN2, LOW);
  digitalWrite(DIR_PIN2, HIGH);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() <= 0) {
    return;
  }

  char command = Serial.read();

  if (command == 'L') {
    digitalWrite(DIR_PIN1, LOW);  // Set direction to left
    stepMotor(STEP_PIN1);
  } else if (command == 'R') {
    digitalWrite(DIR_PIN1, HIGH);  // Set direction to right
    stepMotor(STEP_PIN1);
  } else if (command == 'U') {
    digitalWrite(DIR_PIN2, LOW);  // Set direction to up
    stepMotor(STEP_PIN2);
  } else if (command == 'D') {
    digitalWrite(DIR_PIN2, HIGH);  // Set direction to down
    stepMotor(STEP_PIN2);
  }
}

void stepMotor(int stepPin) {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(STEP_DELAY_US);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(STEP_DELAY_US);
}
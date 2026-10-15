int relayPin = 7;   // or LED pin

void setup() {
  pinMode(relayPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {

  if (Serial.available() > 0) {

    char data = Serial.read();

    if (data == '1') {
      digitalWrite(relayPin, HIGH); // Bulb ON
    }

    if (data == '0') {
      digitalWrite(relayPin, LOW);  // Bulb OFF
    }
  }
}
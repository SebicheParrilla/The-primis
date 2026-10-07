const int LED = 8;
const int INT = 7;



void setup() {

  pinMode (LED, OUTPUT) ;
  pinMode (INT, INPUT_PULLUP) ;
}

void loop() {
  if (digitalRead(INT) == LOW) {
    digitalWrite(LED, HIGH) ;
  }
  if (digitalRead(INT) == HIGH) {
    digitalWrite(LED, LOW) ;
  }
 }

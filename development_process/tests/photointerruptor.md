## Photointerruptor Basics
> Retrospective log from March 13, 2026: This entry's information was digitized from the physical engineering notebook.

We ordered some photointerruptors, what we will later use as RPM sensors for the Pneumatic Engine's Flywheel. To test them we placed them in a breadboard with a arduino UNO, a 220Ω (ohm) resistor, and a green LED. The interruptor's VCC to the 5V pin on the arduino, ground to ground, and the signal header from the sensor to the pin 7 of the arduino, then, pin 8 of the arduino to the anode of the LED and the cathode to the resistor, then ground.

See the component description: [Photointerruptor](../../../hardware/electrical/Cytron_Motion_2350_Pro/Photointerruptor.md)

```cpp
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
```

[interruptor.ino](../../srs/interruptor.ino)

This code turns off the LED when theres an obstruction on the photointerruptor.
## Connection between Raspberry pi and Cytron Motion 2350 with UART

> Retrospective log from May 21, 2026: This entry's information was digitized from the physical engineering notebook.

Since we need a reliable and accurate connection between the Raspberry Pi and the Cytron we will test a connection via UART. This will be escencial to calculate the proper speed, and direction the robot will take.



### Raspberry Pi - Motion 2350 UART Wiring

Logic level: 3.3 V

| Raspberry Pi | Function | Motion 2350 |
|---|---|---|
| GPIO 14 (Pin 8) | TX → RX | GP17 (RX) |
| GPIO 15 (Pin 10) | RX → TX | GP16 (TX) |
| GND (Pin 6) | Ground | GND |

### UART Configuration

- **Raspberry Pi:** UART communication
- **Motion 2350:** UART communication
- **Logic level:** 3.3 V

### Code for both

- **[Cytron](../../../code/srs/CytronUART5212026.py)**
- **[Raspberry Pi](../../../code/srs/RaspiUART5212026.py)** 
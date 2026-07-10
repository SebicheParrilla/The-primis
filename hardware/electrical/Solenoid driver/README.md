# Mosfet Driver Board

Our ASMS uses a [electronic valve](e-valve.md) to interrupt the compressed air being fed to the pneumatic engine, This allows us to turn the engine ON/OFF.

## Voltage problem
This e-valve uses 12V, which is obviously more than our 7.4V batteries, so we used a [voltage booster](voltage_booster.md) to have a 12V power supply for our [electronic valve](e-valve.md).

## Current problem
When our [electronic valve](e-valve.md) is actuated, (letting air through) it has a current draw of aprox. 600mA, if we were to connect the valve directly to a pin of the microcontroller, the microcontroller pin would heat up and possibly get toasted, since a safe amount of current for a pin would be 40mA.


## Mosfet Solenoid Driver

<div align= "center">
<img src="../../../hardware\photos\mosfetdriver.jpg" width=350>
</div>

--- 

To fix this problem we need to actuate a high current circuit with a small current circuit, and the following circuit makes this possible.
<div align= "center">
<img src="../../../hardware\photos\MosfetCircuit.PNG" width=350>
</div>



this circuit uses a MOSFET, (Metal Oxide Semiconductor Field Effect Transistor) labled **M1** in the circuit diagram, this has many configurations, but how we utilized it was aplying 5V to the Gate, to interrupt the Drain current, this means that when theres a 5V signal in the get, the e-valve will not recieve current, therefore be closed and not let air pass.

## Gate driver

But, there a catch, the MOSFET we had available wasnt logic-level, this basicly means that for the drain to be fully interrupted, the gate needed mre than 5V, which we cant supply with a 5V microcontroller pin. To solve this problem we used a gate driver, a secondary circuit to boost voltage from the Gate with a BJT (Bipolar Junction Transistor) labled **Q1** in the circuit diagram. Now we can actuate between ON/OFF with the microcontoller.

## LED indicator 

We used a orange and green LED to indicate the state of the Driver, when the orange LED (labled D2 in the circuit diagram) is on, the gate voltage is high, in other words, the e-valve isnt letting air through. 

When the green LED (labled D3 in the circuit diagram) is on, the solenoid circuit is closed, in other words the solenoid is letting air pass through the system. 
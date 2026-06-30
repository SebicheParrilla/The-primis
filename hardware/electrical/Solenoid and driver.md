# Electronic Solenoid Valve

Our ASMS uses a electronic valve to interrupt the compressed air being fed to the pneumatic engine. 

## Voltage problem
This e-valve uses 12V, which is obviously more than our 7.4V batteries, so we used a Voltage Booster to have a 12V power supply for our e-valve.

## Current problem
When our e-valve is actuated, (letting air through) it has a current draw of aprox. 650mA, if whe were to connect the valve directly to a pin of the microcontroller, the microcontroller pin would heat up and possibly get toasted, since a safe amount of current for a pin would be 40mA.


## Mosfet Solenoid Driver

To fix this problem we need to actuate a high current circuit with a small current circuit, and the following circuit makes this possible.
<div align= "center">
<img src="../../hardware\photos\MosfetCircuit.PNG" width=350>
</div>



this circuit uses a MOSFET, (Metal Oxide Semiconductor Field Effect Transistor) labled **M1** in the circuit diagram, this has many configurations, but how we utilized it was aplying 5V to the Gate, to interrupt the Drain current, this means that when theres a 5V signal in the get, the e-valve will nt recieve current, therefore be closed and not let air pass.

## Gate driver

But, there a catch, the MOSFET we had available wasnt logic-level, this basicly means that for the drain to be fully interrupted, the gate needed mre than 5V, which we cant supply with a basic microcontroller pin. To solve this problem we used a gate driver, a secondary circuit to boost voltage from the Gate with a BJT (Bipolar Junction Transistor) labled **Q1** in the circuit diagram. Now we can actuate between ON/OFF with the mnicrocontoller.

## LED indicator 

We used a orange and green LED to indicate the state of the Driver, when the orange LED (labled D2 in the circuit diagram) is on, the gate voltage is high, in other words, the e-valve isnt letting air through. 

When the green LED (labled D3 in the circuit diagram) 
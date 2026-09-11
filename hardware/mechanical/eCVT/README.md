# eCVT Planetary Transmission System

## Overview

This folder documents the design and theory behind the custom eCVT (electronic Continuously Variable Transmission) system used in the robot. The system is based on a planetary gear set combined with a pneumatic power source and controlled mechanical modulation with an electric motor.

The pneumatic engine is difficult to control directly. The eCVT allows the robot to control the output speed by changing the motion of the ring gear.


### Term glossary 

[Brake Specific Fuel Consumption (BSFC)]()
## Why an eCVT for our pneumatic engine?

### First, lets see the advantages.

<table>
<tr>
<th width="50%">fixed ratio transmissions</th>
<th width="50%">eCVT</th>
</tr>

<tr>
<td>Are constrained to a fixed gear ratio per gear, thus in order to gain speed you need theengine to rev higher than the most efecient BSFC.</td>
<td>eCVT's allow you to have the exact gear ratio you need in order to have the best BSFC. </td>
</tr>

<tr>
<td>The Pneumatic engine's speed is hard to control eficiently and without waisting energy. </td>
<td>Allows you to keep the engine in the most eficient BSFC, and change the robots speed with the electric motor.</td>
</tr>

<tr>
<td> Need a clutch to engage and disengage power from the weels in order to change gears. </td>
<td>No need for gear changing thus no need for power disengaging.</td>
</tr>

<tr>
<td>Hard to have a smooth acceleration and deceleration.</td>
<td>Extremely easy to have a smooth acceleration and deceleration.</td>
</tr>



</table>

### Important tradeoffs

- In order to control the robot's speed, the microcontroller needs reliable measurements of both the pneumatic engine and electric motor speeds. Errors in either measurement can cause incorrect transmission control.
-   A fixed-ratio drivetrain is mechanically simpler and the eCVT depends more on software to coordinate the pneumatic engine, electric motor, and transmission.
- More failure points like bearings, gears, friction points and sensors.



## Gear System Description

The eCVT uses a planetary gear system, consisting of:

- **Sun Gear (S)** – input gear #1
- **Ring Gear (R)** – input gear #2
- **Planet Gears** – distribute load between sun and ring
- **Planet Carrier** – output structure holding planet gears

(Planetary gears can be used in various combinations on inputs/outputs, what was described above is how we used it)

This configuration allows variable torque distribution depending on which elements are fixed or driven.



# eCVT Planetary Transmission System

## Overview

This folder documents the design and theory behind the custom eCVT (electronic Continuously Variable Transmission) system used in the robot. The system is based on a planetary gear set combined with a pneumatic power source and controlled mechanical modulation.

The pneumatic engine is difficult to control directly. The eCVT allows the robot to stabilize or control the output speed by changing the motion of the ring gear.

The biggest advantage to this transmission is being able to combine two inputs on to one output, this allows you to:

- have smooth acceleration and deceleration, because of no constraits over fixed gear ratios
- higher eficiency because of allways being at the perfect gear ratio
- eliminate the need of a clutch to engage or disengage energy


## Gear System Description

The eCVT uses a planetary gear system, consisting of:

- **Sun Gear (S)** – input gear #1
- **Ring Gear (R)** – input gear #2
- **Planet Gears** – distribute load between sun and ring
- **Planet Carrier** – output structure holding planet gears

(Planetary gears can be used in various combinations on inputs/outputs, what was described above is how we used it)

This configuration allows variable torque distribution depending on which elements are fixed or driven.

# Principles of gear creation in CAD softwares

## Gear Module (m)

The module defines the size of the gear teeth:

\[
m = \frac{d}{z}
\]

Where:
- `m` = module
- `d` = pitch diameter
- `z` = number of teeth

Module directly contributes to a gears size and shape.


## Pressure Angle

The pressure angle is the angle at which force is transmitted between gear teeth.

In this system:
- Standard pressure angle: **20°**
- Ensures smooth contact between gear teeth
- Reduces friction and improves efficiency
- Improves load distribution in planetary systems

A consistent pressure angle is required for all meshing gears to avoid binding or wear.


## Proper meshing formula

To ensure correct gear interaction and prevent mechanical interference, the system follows:

(R + S) / (number of planets) = x




Where:
- `R` = ring gear tooth influence
- `S` = sun gear tooth influence
- `P` = number of planets

 (x) must be 1 for it to have proper meshing.

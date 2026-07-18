# Air Supply Duration Calculations 2-28-2026
> Retrospective log: This entry's information was digitized from the physical engineering notebook on 2026-07-16.
## Problem

The [V1.0  pneumatic engine](../hardware\mechanical\Pneumatics\Penumatic_Engine\1.0.md) could only operate for approximately **7 seconds** using one air tank charged to **40 PSI**.

This runtime was too short to complete a full WRO run, so we investigated ways to increase the amount of stored compressed air without increasing tank pressure.


- Tank volume: **237 cm³**
- running time (at 40psi): **7s.**
- absolute pressure(used for calculations) 40+14.7 = **54.7 psia** 
```
The total of energy stored as compressed air can be represented as 
54.7psia x 237cm³.
```


---
### Boyle's law

```
Stored energy as compressed air = Pressure × Volume
```
We can use this principle to store more energy without increrasing volume or displacement of air tanks, which maskes the tanks take more space and weigh more. 

Let's do the same excersise but with 100psi at the tank which the manufactrer indicates has a max of 110psi.

- Tank volume: **237 cm³**
- absolute pressure 100+14.7 = **114.7 psia** 
```
The total of energy stored as compressed air can be represented as 
114.7psia x 237cm³.
```



---
### Run time estimates with different pressures

Comparing the runtime we had and using Boyle's law we can estimate the runtime on a tank pressurised to 100psi, then regulated to 30psi.

$$
t_{\text{new}} = t_{\text{test}} \times \frac{P_{\text{new, abs}}}{P_{\text{test, abs}}}
$$

$$
t_{\text{new}} = 7 \times \frac{114.7}{54.7}
$$

$$
t_{\text{new}} = 7 \times 2.09
$$

$$
t_{\text{new}} \approx 14.6\ \text{s}
$$
$$
\begin{aligned}
t_{\text{new}} &= \text{New runtime} \\
t_{\text{test}} &= \text{Measured test runtime} \\
P_{\text{new, abs}} &= \text{New absolute pressure} \\
P_{\text{test, abs}} &= \text{Measured test absolute pressure}
\end{aligned}
$$
```
Here we basically used the run time from the test and used it as a measure to know how much it would increase at 100psi. Now well calculate this for 4 tanks at 100psi instead of 1.
```
$$
\begin{aligned}
\text{New Runtime} &= 7 \times (2.09 \times 4) \\
\text{New Runtime} &= 7 \times 8.36 \\
\text{New Runtime} &\approx 58.5\ \text{s}
\end{aligned}
$$

58.5 seconds means 19.5 seconds each lap, definitely possible but we need a strong software to make operations fast and reliable.


---
### Analysis
58.5 seconds means 19.5 seconds each lap, definitely possible but we need a strong software to make operations fast and reliable. The calculations assume constant airflow throughout the discharge without restrictions or leaks, the pneumatic engine cannot effectively use air once the tank pressure becomes below 20psi with the normal resistance the robot causes.


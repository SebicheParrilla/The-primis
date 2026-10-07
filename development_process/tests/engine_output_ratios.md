# Pneumatic Engine Gear Ratio Optimization


The overall goal of our entire drivetrain is to conserve as much compressed air as possible, so that the pneumatic engine can have the energy necesary for 3 revolutions and a parking sequence, we needed to research what variables impacted the eficiency and consumption of our precious air pressure.

The main variables we investigated were:

- Operating pressure
- Gear ratio
- Location of the gear reduction
- Flywheel size and mass
- Available torque and output speed

The objective was to find the best balance between **torque, speed and air
consumption**.

We can just keep adidng air tanks to store more air, but thats besides the fact of needing air consumption eficiency.



## Understanding the Pneumatic Engine

During our initial testing, we found that the pneumatic engine could rotate
with very little load at approximately **20 PSI**. However, once  load was
applied, the engine required significantly more torque to continue rotating
and would stall.


Increasing the operating pressure allows the pneumatic engine to produce more
torque and maintain its rotational speed when a load is applied. However,
higher pressure also causes the compressed-air supply to be consumed more
quickly.

This created an important trade-off:

- **Higher pressure:** More available torque and better performance under
  load, but greater air consumption.
- **Lower pressure:** Lower air consumption, but less available power.

Because of this, simply increasing the regulator pressure was not an ideal
solution. We wanted to determine whether the drivetrain gearing could be
optimized to allow the engine to operate at a lower pressure while still
providing enough torque at the wheels.



## Understanding Gear Ratios

A gear ratio changes the relationship between the rotational speed and torque
of the input and output shafts.

For our documentation, we refer to the two configurations as **high gear
ratio** and **low gear ratio** based on the resulting output speed:

### High Gear Ratio

A high gear ratio in our terminology is a configuration where the output
rotates faster than the input.

This can be achieved by using a **larger gear on the input and a smaller gear
on the output**.

The result is:

- Higher output speed
- Lower output torque


In theory, this would allow the robot to travel faster while the engine
rotates more slowly. However, since you sicrifice torque for speed, this configuration requires a lot of torque to turn in to speed.

Since our pneumatic engine produces relatively low torque, a
high output-speed ratio can cause the engine to struggle or stall when the
robot is under load.

### Low Gear Ratio

A low gear ratio in our terminology is a configuration where the output
rotates slower than the input.

This can be achieved by using a **smaller gear on the input and a larger gear
on the output**.

The result is:

- Lower output speed
- Higher output torque

This configuration is useful when the engine does not produce enough torque
to move the robot.

However, one must sacrifice speed for all the torque gain. If the
reduction is too large, the robot may have enough torque to move but will be
very slow.

## Mechanical constraints

Since our compressed-air supply is limited, we initially considered using
gearing to reduce the amount of work the pneumatic engine needed to perform.

The idea was to allow the engine to operate at a suitable speed while using
the transmission to convert its rotational speed into the torque required at
the wheels.

However, gearing does not create energy. In an ideal system, gearing trades
rotational speed for torque while maintaining the same mechanical power.

In a real system, additional gear stages introduce mechanical losses through
friction, bearing resistance, tooth contact, and other sources.

Therefore, simply increasing the gear ratio does not automatically make the
system more efficient.

The goal was instead to determine which gear ratio allowed the pneumatic
engine to operate most effectively while maintaining sufficient wheel torque.


## Flywheel and Gear Ratio Placement

Another variable we needed to  consider was **where to apply the gear ratio**.

Our pneumatic engine uses a flywheel that can store rotational kinetic energy.
This led us to consider whether we could make the flywheel rotate at a high
speed using a high gear ratio.

The theoretical concept was:

**Pneumatic Engine → High-Speed Gear Ratio → Flywheel → Low Gear Ratio → Wheels**

The first ratio would increase the rotational speed of the flywheel, allowing
it to store more rotational kinetic energy. The second ratio could then reduce
the flywheel's speed and provide greater torque to the drivetrain.

This appeared promising because the flywheel could potentially act as an
energy buffer between the pneumatic engine and the wheels.


# In Reality

## Flywheel Testing

However, the flywheel we are using doesnt store energy very well, for it to store energy it would need to be way heavier, although it smoothes out the pneumatic engines power inconsistencies.

Because of this its not very efective because escencially we were just increasing and decreasing the gear ratio, introducing mechanical loss.

Despite this, the flywheel provided two important benefits.

First, its rotational inertia helped **smooth the power output of the
pneumatic engine**. Instead of the engine's power output producing as much
variation in rotational speed, the flywheel helped maintain smoother
rotation.

Second, the larger diameter of the flywheel improved the resolution of our
optical RPM measurement. The photoelectric interrupter could detect the
encoder features over a larger physical circumference, producing a more
useful signal for calculating RPM.

Because of these advantages, the flywheel remained useful even though it did
not provide significant propulsion after the engine stopped.

---

## Initial Gear Ratio Test

We then tested whether the pneumatic engine could reliably drive the robot
using a **1:1 ratio from the crankshaft to the engine output** and a **1:1
ratio from the flywheel to the transmission input**.

At this point, the drivetrain contained:

- Crankshaft → Engine output: **1:1**
- Flywheel → Transmission input: **1:1**
- V5.0 Transmission: **1:8.4**
- Differential: **1.4:1**

The transmission and differential therefore provided a total 
reduction of:

$$
8.4 \times 1.4 = 11.76
$$

This resulted in an overall ratio of approximately:

**11.76:1 from the engine output to the wheels.**

Even with this significant torque multiplication, the pneumatic engine was
not able to move the robot reliably at the target operating pressure.

This was an important result because it demonstrated that the main limitation
was not simply the lack of transmission reduction. The pneumatic engine had
a relatively low torque output, and the drivetrain needed to be carefully
matched to its operating characteristics.

---

## Balancing Pressure and Gear Ratio

After the initial test, we began balancing the two main methods of increasing
the available wheel torque:

**Increasing pressure** or **increasing mechanical reduction**.

Increasing pressure allowed the pneumatic engine to produce more torque and
better resist the load, but consumed compressed air faster.

Increasing the reduction increased the torque available at the wheels, but
reduced the vehicle's output speed.




## Final Configuration

Through testing, we found that this gear ratio provided a much better
balance.
- Crankshaft → Engine output: **1:1**
- Flywheel → Transmission input: **1:4**
- V5.0 Transmission: **1:8.4**
- Differential: **1.4:1**

The transmission and differential therefore provided a total 
reduction of:

$$
8.4 \times 1.4 \times 1.4 = 16.464
$$

This configuration allowed the pneumatic engine to operate at approximately
**25 PSI** while maintaining reliable movement of the robot.

Instead of increasing the regulator pressure, we used the
mechanical gearing to provide additional torque where it was needed, without wasting air pressure.

We of course lost speed, but in order to even move the robot at a total gear reduction of 11.46:1 we needed to raise pressure to more than **32PSI**.




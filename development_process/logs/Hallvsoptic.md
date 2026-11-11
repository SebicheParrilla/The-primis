# Encoder Selection: Photointerrupter vs. Hall Effect Sensor

## Design Rationale

During the development of Aiza V3, we evaluated two sensing technologies for measuring the rotational speed of the pneumatic engine's flywheel: a **photointerrupter** and a **Hall effect sensor**.

Both technologies can detect rotational movement and generate pulses that can be used to calculate RPM.

We ultimately selected a **photointerrupter** because it offered a simpler, lighter, and more cost-effective solution for our application.

The photointerrupter works by emitting infrared light toward a photodetector. As the slotted encoder disc rotates, its slots periodically interrupt the light beam, generating electrical pulses. By counting these pulses over time, the controller can calculate the flywheel's rotational speed.

A Hall effect sensor detects changes in magnetic fields. A typical implementation would require permanent magnets attached to the rotating assembly. This introduces additional hardware and mounting considerations.

## Advantages, Disadvantages & Trade-offs

| Design consideration | Photointerrupter | Hall effect sensor |
|---|---|---|
| **Cost** | Generally inexpensive and widely available. | Can be more expensive depending on sensor type and required magnetic components. |
| **Weight** | Lightweight; only requires a small sensor and encoder disc. | May require additional magnets or a magnetic target, increasing assembly weight. |
| **Mechanical complexity** | Requires a slotted encoder disc and precise sensor alignment. | Requires magnets and secure mounting. |
| **Material requirements** | Encoder disc can be manufactured from lightweight plastic or other opaque materials. | Magnetic sensing requires a suitable magnetic field. Ordinary nonmagnetic metals such as aluminum will not work as magnetic targets. |
| **Power consumption** | Requires continuous power for its infrared emitter. | Typically low power consumption, depending on sensor architecture. |
| **Signal generation** | Generates pulses when the encoder disc interrupts the infrared beam. | Generates pulses or changes in output when the magnetic field changes. |

## Engineering Trade-offs

The primary advantage of the photointerrupter was its ability to provide accurate rotational feedback without introducing additional rotating hardware such as magnets.

Its low weight was particularly important because Aiza V3 operates under strict competition weight constraints. Using a lightweight encoder disc allowed us to obtain rotational measurements without unnecessarily increasing the mass of the flywheel assembly.

Additionally, the photointerrupter was considerably more economical, allowing us to allocate resources to other components of the robot.

However, this decision involved a trade-off in environmental resistance. Unlike Hall effect sensors, photointerrupters depend on an unobstructed optical path. Dust accumulation, mechanical misalignment, or damage to the encoder disc could interfere with readings.


## Final Decision

The photointerrupter was selected because it provided the best balance between cost, weight, mechanical simplicity, and measurement capability for Aiza V3.

Although Hall effect sensors offer better resistance to optical obstructions and eliminate the need for an optical encoder disc, their additional magnetic hardware and mounting requirements were not justified for this application.

Ultimately, the photointerrupter fulfilled our rotational feedback requirements while minimizing unnecessary mechanical complexity and mass.
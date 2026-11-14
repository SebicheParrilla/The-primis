


## Chassis V.4 Design

The chassis is the fourth iteration, it serves as the structural foundation of AIZA, supporting the drivetrain, steering mechanism, pneumatic system, electronics, and sensors. Its design must accommodate the robot's mechanical and electrical components while maintaining sufficient rigidity and stability for autonomous operation.

<div align= "center">
<img src="../media/photos/Chassis.jpeg" width=500>
</div>

### Design Considerations

Several factors influenced the chassis design:

- **Component integration:** Provide mounting locations for the pneumatic engine, eCVT, differential, steering mechanism, air tanks, batteries, and controllers.


- **Packaging constraints:** Fit all components within the competition's dimensional restrictions while maintaining accessibility for assembly and maintenance.
- **Serviceability:** Allow components to be removed, adjusted, or replaced without requiring extensive disassembly of the robot.
- **Sensor positioning:** Provide stable mounting locations that preserve the camera's field of view and not shake when acelerating and decelerating


### Design Trade-offs

| Design consideration | Benefit | Trade-off |
|---|---|---|
| Structural rigidity | Maintains component alignment and reduces deformation | Can increase material usage and weight |
| Fits everything within the bundries | Complies with WRO rules!| Almost most mass is concentrated in the ASMS, and on top of that it sit above the Steering system connections |
| Modular mounting | Allows individual subsystems to be removed or modified | Can introduce additional fasteners and complicate things |

### Assembly and Reproducibility

The chassis manufacturing files and assembly instructions are provided in the repository:

- [Mechanical CAD files](../media/CAD/STL/Car_Frame_3.stl)
- [Vehicle iterations](../development_process/vehicle_iterations)


# World Robot Olympiad Future Engineers 2026
Welcome to our repository, we are a team from Puerto Rico that tackled for the first time the challenge of the WRO future engineers category, determined to bring a unique aproach to the competition.

All terms in the italic font are linked to the [*glossary*](Glossary.md).


# The Primis


<div align= "center">
<img src="media/team_photos/PrimistoPanama.jpeg"width=450>
</div>


### Team Members,  From Left to Right:

1. Joseph Macias Diaz
2. York E. jackobs Lopez **(Coach)**
3. Sebastian J. Parrilla
4. Carlos A. Espada Rivera

### [team history](team_history.md)
# Anti Insult Zapping Automaton (A.I.Z.A)
AIZA is our autonomous robot featuring an [*electropneumatic*](Glossary.md) hybrid [*drivetrain*](Glossary.md) and [*vision-based navigation*](Glossary.md) developed for the **WRO Future Engineers 2026** competition.


<table>
  <tr>
    <td align="center">
      <b>Front View</b><br>
      <img src="media\photos\AIZA_Front.jpeg" width="230">
    </td>
    <td align="center">
      <b>Rear View</b><br>
      <img src="media\photos\AIZA_Back.jpeg" width="230">
    </td>
    <td align="center">
      <b>Left Side</b><br>
      <img src="media\photos\AIZA_Left.jpeg" width="230">
    </td>
  </tr>
  <tr>
    <td align="center">
      <b>Right Side</b><br>
      <img src="media\photos\AIZA_Right.jpeg" width="230">
    </td>
    <td align="center">
      <b>Top View</b><br>
      <img src="media\photos\AIZA_Top.jpeg" width="230">
    </td>
    <td align="center">
      <b>Bottom view</b><br>
      <img src="media\photos\AIZA_Bottom.jpeg" width="230">
    </td>
  </tr>
</table>


### [Click here to see past iterations of the robot](development_process/vehicle_iterations)

[**ALL CAD files**](media\CAD)


Unlike a conventional electric drivetrain, AIZA uses a [*pneumatic engine*](Glossary.md) as its primary source of [*mechanical power*](Glossary.md). Multiple systems, like the [*Air Supply and Management System*](Glossary.md) (ASMS), sensor system and electrical system are used to control and monitor the drivetrain, while a [*electronic continuously variable transmission*](Glossary.md) (eCVT), allows the pneumatic engine's power to be adapted eficiently to the robot's operating demands and conditions.

*Mention navegation sensors too
### [The complete step by step guide to build your very own AIZA here.](build_guide/Step01/Step01.md)

## Performance videos
Open challenge:
[(Placeholder)]()

Obstacle challenge:
[(Placeholder)]()






# Systems Architecture

AIZA is divided into four main systems that work together as a single autonomous platform:

 **Mechanical System** - Converts pneumatic and electrical power into controlled and measured wheel motion through the drivetrain.

 **Air Supply and Management System** - Stores compressed air, [*regulates*](Glossary.md) the pressure, and supplies the pneumatic engine.

 **Electrical System** - Provides power to the Raspberry Pi, Cytron Motion 2350, sensors, [*actuators*](Glossary.md), and the electric transmission motor.
 
 **Sensing and Control System** - Uses the camera, [*IMU*](Glossary.md), and [*encoders*](Glossary.md) to determine the robot's position, orientation, and drivetrain state.

<div align= "center">
<img src="media/photos/SystemArchitecture.PNG"
width=450>


</div>


# Mechanical


### Chassis 

The chassis is the fourth iteration, it serves as the structural foundation of AIZA, supporting the drivetrain, steering mechanism, pneumatic system, electronics, and sensors.

<div align= "center">
<img src="media/photos/Chassis.jpeg" width=500>

[more on it here](mechanical/Chassis.md)
</div>

### Steering

Our steering system needed to be robust since we knew from the start the robot was going to be heavy and big, it had to be made separate from the cassis since our printer didn't have enough space to print the full chassis.

<div align= "center">
<img src="media\photos\Steering.jpeg
" width=500>

[more on it here](mechanical/Steering.md)
</div>



### The Pneumatic Engine

Our robot uses a 4 piston, 2 [*crankshaft*](Glossary.md) pneumatic engine. It has a [*flywheel*](Glossary.md) that smoothes out how the engine spins with [*inertia*](Glossary.md), we made it with slots in order to count the interruptions per second with the [*Photointeruptor*](Glossary.md) RPM sensor, which lets us know how fast its going **(more on that later)**.

[**Click here to understand engine fundamentals**](mechanical\Pneumatics\Penumatic_Engine\README.md)

[**Click here to see past iterations of the engine**](mechanical/Pneumatics/Penumatic_Engine)
<div align= "center">
<table>
  <tr>
    <td><img src="media/photos/pneng2.1back.jpg" width="340"/></td>
    <td><img src="media/photos/pneuma2.1.jpg" width="340"/></td>
  </tr>
  <tr>
    <td align="center">Front view</td>
    <td align="center">Back view</td>
  </tr>
</table>
</div>

From the output of the flwyheel, to the output of the pneumatic engine we used a 1.4:1 gear ratio, [**click here to see why we chose this**](development_process/tests/engine_output_ratios.md).

### A.S.M.S (Air Supply and Management System)
The ASMS stores compressed air in a tank assembly with a combined internal [*displacement*](Glossary.md) of 1,422 cm³, charged to 100 [*psi*](Glossary.md). A pressure regulator reduces the stored air pressure to a nominal operating pressure of 20 psi before supplying the pneumatic engine. Storing the air at a higher pressure was escential for a longer runtime [click here to see how we tested that](development_process/tests/air_supply_duration_calculations.md).


 A normally closed, electronic valve controls air delivery to the engine, remaining closed until electrically energized by the robot's control system.






 <div align= "center">
<img src="media/photos/Flowchart ASMS.PNG" width=600>

</div>




</td>
</tr>
</table><table>
<tr>
<td width="50%" align="center">

<img src="media/photos/Airtanksx6.jpeg" width="300">

</td>
<td width="60%" valign="top">

We store the compressed air in 6 lightweight tanks at 100psi of pressure, and join them all with silicone tubing and "T" adapters.

[why we used it and more details here.](mechanical/eCVT/README.md)
</td>
</tr>
</table>

<div align= "center">
<img src="media\photos\ASMS.jpeg" width=500>
</div>



### Pneumatic System Pressure Ratings and Safety Margins

| Component | Maximum Rated Pressure (PSI) | Operating Pressure (PSI) | Safety Margin (PSI) |
|:--|--:|--:|--:|
| Pneumatic Air Tanks | 110 | 100 | 10 |
| Pressure Regulator | 145 | 25 | 120 |
| Pneumatic Engine (Low Pressure Hoses) | 40 | 25 | 15 |
| E-Valve  | 115 | 25 | 90 |
| NPT M¼ to NPT F⅛  brass fitting | 1200 | 100 | 1100 |
| NPT M¼ to NPT M⅛ | 1200 | 100 | 1100 |
| Brass T fitting, 2x F⅛, 1x M⅛| 1200 | 100 | 1100 |
| NPT M⅛ to ¹⁄₁₆ hose barb| 120 | 100 | 20 |
| NPT M⅛ schrader valve| 200 | 100 | 100 |
| High pressure hoses and conectors| 120 | 100 | 20 |



Note that the manufacturer's max pressure isn't the [*burst pressure*](Glossary.md), they normally have some headroom before a total failure, so safety the safety margin is actually more.



## The challenges of a pneumatic engine in a autonomous robot
A conventional electric drivetrain is simpler, more efficient, easier to control, and generally better suited for an autonomous competition robot than a penumatic engine. Rather than treating the disadvantages of pneumatic power as reasons to avoid it, we treated them as engineering challenges.


But we knew that the limitations of a pneumatic drivetrain were not necessarily limitations of the pneumatic engine alone, but of how the entire drivetrain was designed around it.


<table>
<tr>
<th width="50%">Disadvantage</th>
<th width="50%">Our Approach</th>
</tr>

<tr>
<td>Hard to control the pneumatic engine's speed with a reliable, leak free, compact, and lightweight solution.</td>
<td>An eCVT allows you to keep the pneumatic engine on a fuel eficient speed while changing the speed of the robot with the secondary electric motor.

[**Click here to see how we proved this with our own custom engine dyno**](development_process/tests/DYNAMOMETER.md)</td>
</tr>

<tr>
<td>A system capable of continuously supplying compressed air to the pneumatic engine would be expensive, heavy, and consume valuable space on the robot.</td>
<td>Rather than supplying compressed air continuously, we designed the robot around stored compressed air using lightweight, high pressure tanks and a way to regulate the air, allowing the pneumatic engine to operate independently of an onboard compressor.</td>
</tr>



<tr>
<td> Pneumatic engine can only spin a certain direction, depending of how timing is set up.  </td>
<td>Instead of reversing the pneumatic engine, we designed the drivetrain so that reverse motion is handled electrically through the eCVT. This allows the pneumatic engine to remain optimized for forward operation while maintaining bidirectional control of the robot.</td>
</tr>



</table>

### The eCVT 5.1





</td>
</tr>
</table><table>
<tr>
<td width="50%" align="center">

<img src="media/photos/eCVT5.1.jpeg" width="300">

</td>
<td width="60%" valign="top">

An **eCVT** is a electronic continuosly variable transmission, a transmission that pairs two inputs in to a output, and with the proper combining of the inputs, a output with an infinite [*gear ratio*](Glossary.md) is possible without the need of gear shifting. 

[Click here to see why we used it](mechanical/eCVT/README.md)

[See the past iterations of the eCVT!](mechanical\eCVT)
</td>
</tr>
</table>






</td>
</tr>
</table><table>
<tr>
<td width="50%" align="center">

<img src="media/photos/mokeblockmotor1.jpg" width="300">

</td>
<td width="60%" valign="top">

The second input for the eCVT is this, a makeblock 7.4V Motor with a built in encoder, this allows us to know precisely at what RPM its spining, which is escential for eCVT logic.

[More on calculated gear ratios on software.]()

</td>
</tr>
</table>

# Dynamometer

Since one of the best features of our custom eCVT is the ability to keep the pneumatic engine on a fuel eficient speed while changing the speed of the robot with the secondary electric motor, we needed to know which was the most eficient speed of the pneumatic engine.

We built a custom dynamometer to measure the engine's [*torque*](Glossary.md), [*rotational speed*](Glossary.md), and [*horsepower*](Glossary.md) at different regulator operating pressures. This allowed us to evaluate the trade-off between engine performance and air consumption.

 

<table>
  <tr>
    <td width="40%" valign="top">
      <img src="media/photos/DynoTorque.png" width="100%">
    </td>
    <td width="60%" valign="top">
      <h3>Max Torque</h3>
      <p>
        A load cell measures the reaction force generated by the
        braking mechanism, allowing torque to be calculated.
      </p>
    </td>
  </tr>
    <tr>
    <td width="40%" valign="top">
      <img src="media/photos/DynoRPM.png" width="100%">
    </td>
    <td width="60%" valign="top">
      <h3>Max RPM</h3>
      <p>
        An optical sensor tracks the engine's rotational speed
        throughout the testing process.
      </p>
    </td>
  <tr>
    <td width="60%" valign="top">
      <img src="media/photos/DynoPower.png" width="100%">
    </td>
    <td width="40%" valign="top">
      <h3>Max Power</h3>
      <p>
        With the calculated torque, and the RPM of the engine, we calculated the power.
      </p>
    </td>
  </tr>
  </tr>
    <tr>
    <td width="60%" valign="top">
      <img src="media/photos/DynoStamina.png" width="100%">
    </td>
    <td width="40%" valign="top">
      <h3>Operation Duration</h3>
      <p>
        This chart represents how the air supply duration is affected by the operating air pressure.
      </p>
    </td>
    
  </tr>
</table>

### Selecting the optimal operating pressure

| Pressure | Advantages | Disadvantages | Trade-off |
|---|---|---|---|
| **15 PSI** | Low air consumption | Low rotational speed, torque and power could not be measured | Greater potential endurance, but very limited performance |
| **20 PSI** | Measurable torque and power moderate operating pressure | Lower maximum output than higher-pressure settings | Sacrifices peak performance in favor of a more longer runtime |
| **25 PSI** | Higher torque, power, and speed than at 20 PSI | Greater air consumption and reduced runtime | Improved performance at the expense of air endurance |
| **30 PSI** | Highest measured torque, power, and rotational speed | Higher air consumption and shorter runtime | Maximizes instantaneous performance rather than endurance |

### Selected operating pressure: **20 PSI**

Although 30 PSI provided the highest measured power output, we selected 20 PSI to prioritize air endurance over maximum instantaneous performance. This provides a compromise between mechanical output and the available compressed-air supply.
The data shows a fairly clear trend: increasing pressure improves the pneumatic engine's performance, but it comes at the cost of operating duration. That's a  trade-off to discuss because we're not simply trying to maximize power, we're balancing performance against available stored energy.

### Dyno results at 20psi

|  | 20 PSI |
|---|---|
| Maximum Torque | 0.015 N·m |
| Maximum Power | 0.0002 HP |
| Maximum Speed | 304 RPM |
| No-Load Runtime | 50 s |

# Power and Sensor Architecture

AIZA's power and sensing architecture was designed around the electrical requirements of its electropneumatic drivetrain and autonomous navigation system. The electrical system supplies three voltage levels to the robot's components, while the sensing system provides feedback for drivetrain control, orientation measurement, distance detection, and computer vision.

This section documents the power distribution, electrical design decisions, sensor selection, calibration, and reliability considerations.

## 1. Power Distribution and Electrical Architecture

### Voltage Regulation

AIZA's electrical components require three different voltage levels. Instead of powering every component directly from the battery, we use voltage conversion to provide the required supply rails.

| Voltage rail | Source | Purpose |
|---|---|---|
| 7.4 V | Two 3.7 V cells connected in series | Main battery supply and components operating at battery voltage |
| 5 V | Buck converter stepping down from 7.4 V | Raspberry Pi and 5 V electronics |
| 12 V | Voltage booster stepping up from 7.4 V | Solenoid valve |

The voltage regulators are shown below.

![Voltage regulators](media/photos/Voltageregulators.PNG)

The use of separate voltage rails allows components with different operating requirements to share the same battery system.

### Battery Configuration and Capacity Constraints

The robot uses interchangeable 7.4 V battery packs with a nominal capacity of 3.5 Ah.

Due to the limited mass and available space within the chassis, increasing onboard battery capacity was not practical within the current design constraints. Instead, battery packs are swapped and recharged between competition runs.

Battery capacity alone does not determine whether a pack can safely supply the robot's peak current. Its discharge rating and voltage behavior under load must also be considered when evaluating the power system.

### Power Budget and Current Distribution

A component-by-component current budget was used to estimate the electrical demand of the robot.

![Maximum current calculations](media/photos/CurrentTable.PNG)

The current budget should account for both normal operating current and peak demand, particularly during motor acceleration and simultaneous actuator operation.

The relevant quantities are:

- Component operating voltage.
- Typical operating current.
- Maximum or stall current, where applicable.
- Total current demand on each voltage rail.
- Converter output-current ratings.
- Battery discharge capability.

The total demand must be evaluated separately for each voltage rail. A converter must be capable of supplying the combined load connected to its output, including transient demand.

The current calculations are used to evaluate whether the battery and voltage converters can support the robot's electrical loads without excessive voltage drop or interruption of controller operation.

## 2. Actuator Electronics and Solenoid Driver

### Solenoid Valve Driver

The Air Supply and Management System (ASMS) uses an electrically actuated valve to control the delivery of compressed air to the pneumatic engine.

The solenoid requires 12 V and approximately 800 mA. Since the Cytron's control signal cannot directly supply this load, we designed a dedicated driver circuit to switch the higher-current solenoid circuit.

![MOSFET solenoid driver](media/photos/mosfetdriver.jpg)

The driver uses a MOSFET to control the solenoid through a low-current control signal. Because the selected MOSFET is not a logic-level device, a gate driver is used to provide the required gate voltage.

The circuit also includes two LEDs to indicate its operating state and a diode for electrical protection.

![MOSFET driver circuit](media/photos/MosfetCircuit.PNG)

**Further documentation:** [Solenoid driver design and circuit details](electrical/Cytron_Motion_2350_Pro/Solenoid_driver/README.md)


<div align= "center">
<img src="media/photos/electriccomponentdiagram.png" width="600">
</div>
electrical diagram of the components


## 3. Sensor Architecture and Selection

AIZA uses several sensors to obtain information about its environment and drivetrain. Each sensor was selected according to the type of measurement required and the constraints of its application.

| Sensor | Main purpose | Controller |
|---|---|---|
| IMX708 camera | Detects field boundaries and colored markings | Raspberry Pi 3B+ |
| BNO085 IMU | Measures robot orientation and yaw | Cytron Motion 2350 Pro |
| Ultrasonic distance sensor | Measures distance to nearby objects | Cytron Motion 2350 Pro |
| Photointerrupter | Measures pneumatic engine flywheel RPM | Cytron Motion 2350 Pro |
| Electric motor encoder | Measures transmission motor rotation and RPM | Cytron Motion 2350 Pro |

### Camera Selection: IMX708 vs OV5647

The robot initially used an OV5647 camera. During testing, we found that its 56° field of view did not provide enough visual coverage of the walls and surrounding field geometry.

We therefore upgraded to the IMX708, which provides a 120° field of view. The wider field of view allows more of the surrounding environment to be captured in a single image, providing additional visual information for navigation.



<div align= "center">
<table>
  <tr>
    <td><img src="media/photos/Highfov.PNG" width="340"/></td>
    <td><img src="media\photos\LowFov.PNG" width="340"/></td>
  </tr>
  <tr>
    <td align="center"> IMX708  120° </td>
    <td align="center"> OV5647  56° </td>
  </tr>
</table>
</div>

| Camera | Field of view |
|---|---:|
| OV5647 | 56° |
| IMX708 | 120° |

The IMX708 captures images at 2304 × 1296 pixels. A 640 × 360 preview is used to reduce the processing required for visualization.

**Documentation:** [IMX708 specifications](electrical/Raspberry_π_3B+/Camera/IMX708.md)

### Flywheel RPM Sensor: Photointerrupter vs Hall-Effect Sensor

The pneumatic engine's rotational speed must be measured to control the eCVT. We considered optical and Hall-effect sensing methods for this measurement.

The selected photointerrupter detects interruptions in a light path as slots in the flywheel disk pass through the sensor. This provides repeated measurement events during each revolution without requiring a magnetic target.

A Hall-effect sensor detects changes in a magnetic field and would require an appropriate magnetic target and mounting arrangement.

We selected the photointerrupter because it works directly with the slotted flywheel design and provides multiple pulses per revolution.

**Design comparison and trade-offs:** [Photointerrupter vs Hall-effect sensor](development_process/logs/Hallvsoptic.md)

### Electric Motor Encoder

The electric transmission motor has an integrated encoder. Its measurements provide feedback about motor rotation and RPM, allowing the Cytron to adjust the electric input of the eCVT.

The encoder feedback is used together with the pneumatic engine's flywheel RPM measurement to regulate the transmission.

**Related development:** [eCVT logic testing](development_process/tests/eCVT%20logic%20coding.md)

## 4. Sensor Placement and Field Coverage

Sensor placement affects the quality and usefulness of the information received by the controllers.

The camera's wide field of view was an important factor in its selection because the robot needs to observe field boundaries and colored markings while navigating. The upgrade from the OV5647 to the IMX708 was made after testing revealed insufficient visual coverage with the original camera.

The remaining sensors serve different measurement purposes:

- The IMU provides orientation information for heading and turning control.
- The ultrasonic sensor measures distance to nearby objects.
- The photointerrupter is positioned at the pneumatic engine flywheel to measure its rotational speed.
- The motor encoder provides rotational feedback from the electric transmission input.

A complete sensor-placement diagram should identify each sensor's physical location, orientation, and measurement direction relative to the chassis and competition field.

## 5. Sensor Calibration and Signal Processing

### Camera Calibration and Color Thresholding

The camera's image-processing pipeline uses grayscale thresholding and HSV color segmentation to identify field boundaries and colored markings.

HSV thresholds were established by sampling the colors as they appeared through the actual camera. This accounts for differences between ideal color values and the values captured under the lighting conditions encountered during testing.

The image-processing development included:

1. Separating the white drivable region from the black surrounding boundaries.
2. Extracting contours to identify the field geometry.
3. Processing boundary transitions.
4. Applying HSV thresholds to isolate blue and orange markings.
5. Using the detected markings as navigation inputs.

**Development and testing:** [Mat detection and threshold development](development_process/tests/matthreshholddetecting.md)

### Pneumatic Engine RPM Calibration

The photointerrupter measures the time between consecutive interruptions of its optical path.

The flywheel's known number of slots per revolution is used to convert the measured pulse interval into rotational speed. The measurement code was developed progressively, incorporating pulse counting, interval measurement, averaging, and timeout handling.

**Development and testing:** [Flywheel RPM sensor development](development_process/tests/Flywheelencoder.md)

### IMU and Distance Sensor Calibration

The IMU and ultrasonic distance sensor provide measurements used by the robot's control system. Their calibration procedures, measurement limits, and any filtering or correction applied to their readings should be documented alongside the final sensor configuration.

## 6. Sensor Reliability and Failure Considerations

Sensor reliability is important because inaccurate measurements can affect both navigation and drivetrain control.

The main considerations for AIZA include:

| Component | Potential issue | Engineering consideration |
|---|---|---|
| Camera | Changes in lighting, shadows, and color appearance | Thresholds must be tested under representative field conditions |
| IMU | Measurement noise or orientation drift | Validate yaw readings and heading behavior during turns |
| Ultrasonic sensor | Invalid or inconsistent distance measurements | Define valid measurement limits and behavior for invalid readings |
| Photointerrupter | Missed pulses or inconsistent readings | Use interval averaging and a timeout for stopped-engine detection |
| Motor encoder | Inconsistent or noisy RPM readings | Validate encoder measurements and their effect on transmission control |
| Voltage regulators | Output voltage drop under peak load | Verify voltage stability during simultaneous component operation |
| Battery | Voltage sag or insufficient discharge capability | Validate performance under peak electrical demand |

During development, the camera was upgraded to improve visual coverage, and the flywheel RPM measurement code was refined to improve measurement stability.

The eCVT development tests also exposed inconsistent readings from the motor encoder. This demonstrated the importance of validating sensor feedback before relying on it for closed-loop drivetrain control.

Further reliability testing should document the measured behavior of each sensor under realistic operating conditions, including the response to invalid readings and communication interruptions.

## 7. Electrical and Sensor Integration

The Raspberry Pi and Cytron Motion 2350 Pro divide the sensing and control tasks between two controllers.

The Raspberry Pi processes camera images and determines navigation commands. The Cytron reads the IMU, distance sensor, and drivetrain encoders while controlling the transmission motor and solenoid.

The controllers exchange information through a 3.3 V UART connection.

**Communication development and testing:** [UART connection tests](development_process/tests/UART.md)

The electrical, sensing, and software systems therefore operate as interconnected subsystems: sensor measurements provide feedback to the control system, while the electrical architecture supplies the power required by the controllers and actuators.








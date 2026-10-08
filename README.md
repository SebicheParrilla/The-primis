# The Primis

We are a team from Puerto Rico that tackled for the first time the challenge of the WRO future engineers category, determined to bring a unique aproach to the competition.

<div align= "center">
<img src="t-photos\photos\PrimistoPanama.jpeg"width=450>
</div>


### Team Members,  From Left to Right:

1. Joseph Macias Diaz
2. York E. jackobs Lopez **(Coach)**
3. Sebastian J. Parrilla
4. Carlos A. Espada Rivera

### [t-photos's README](t-photos/README.md)
# Anti Insult Zapping Automaton (A.I.Z.A)
AIZA is our autonomous robot featuring an electropneumatic hybrid drivetrain and vision-based navigation developed for the **WRO Future Engineers 2026** competition.

<div align= "center">
<img src="v-photos\Past_iterations\AIZA 2.1.jpg
"width=450>

(Placeholder)
</div>


Unlike a conventional electric drivetrain, AIZA uses a pneumatic engine
as its primary source of mechanical power. Multiple systems, like the Air Supply and Management System, sensor system and electrical system are used to control and monitor the drivetrain, while a **electronic continuously variable transmission** allows the pneumatic power to be adapted eficiently to the robot's operating demands and conditions.

### [The complete guide to build your very own AIZA here.]()




# Systems Architecture

AIZA is divided into four main systems that work together as a single autonomous platform:

 **Mechanical System** - Converts pneumatic and electrical power into controlled and measured wheel motion through the drivetrain.

 **Air Supply and Management System** - Stores compressed air, regulates the pressure, and supplies the pneumatic engine.

 **Electrical System** - Provides power to the Raspberry Pi, Cytron Motion 2350, sensors, actuators, and the electric transmission motor.
 
 **Sensing and Control System** - Uses the camera, IMU, and encoders to determine the robot's position, orientation, and drivetrain state.

The Raspberry Pi acts as the desition maker, processing the camera and navigation data and commanding the Cytron Motion 2350. The Cytron handles the drivetrain control, including the electric transmission motor, steering servo, pneumatic engine solenoid, and encoder.

# Mechanical


### The challenges of a pneumatic engine in a autonomous robot
A conventional electric drivetrain is simpler, more efficient, easier to control, and generally better suited for an autonomous competition robot than a penumatic engine. Rather than treating the disadvantages of pneumatic power as reasons to avoid it, we treated them as engineering challenges.


But we knew that the limitations of a pneumatic drivetrain were not necessarily limitations of the pneumatic engine alone, but of how the entire powertrain was designed around it.


<table>
<tr>
<th width="50%">Disadvantage</th>
<th width="50%">Our Approach</th>
</tr>

<tr>
<td>Hard to control the pneumatic engine's speed with a reliable, leak free, compact, and lightweight solution.</td>
<td>An eCVT allows you to keep the pneumatic engine on a fuel eficient speed while changing the speed of the robot with the secondary electric motor. </td>
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



# Electrical



- Diagram and component  verview, current calculations
- Safety 




# Sensors, Software and Strategy

#### Before Starting
Complying with the rules, the robot switches to ON with one switch, and initialices the program with one button, once the robot is powered, it initializes UART communication. The Cytron waits until the RaspberryPi boots and sends a "1" as a "ready" signal, after this the RaspberryPi waits until we initialize the program with one of the on-board buttons of the Cytron, when pressed, the Cytron sends a "1" as a "Start" command, which inicializes the vision program, and resets the yaw angle to 0.

#### Navigation State Machine
The robot's IMX708 camera detects line colors and wall boundries, we use this to determine how far the blue or orange line are and which comes first, since its a queue for what direction the robot should go. 

#### Speed State Machine
Depending on the Navigation State Machine value, the RaspberryPi will send the Cytron a speed value of 1-7, using the electric motor encoder and pneumatic engine flywheel encoder the Cytron calculates the correct gear ratio to move the at the speed the RaspberryPi is commanding.

#### After Starting
 After the Cytron sends the start command to the RaspberryPi, the robot goes forward, the camera logic traces a line from the bottom center of the image until it reaches a blue or orange line, it will record the first line that it encounters and keeps track of the distance in pixels with how long the line is, when the line length in pixels is less than 50 pixels, it saves  the yaw angle and then turns, when the yaw angle is more than 90 it recenters and then keeps going straight, then we repeat that 11 times to complete the open challenge.








# Glossary

Our robot takes readings of various sensors in order to determine the right decision in the play field.

#### IMX708 Camera
A camera capable of outputting an image with a 120° FOV.

[IMX708's specs](hardware/electrical/Raspberry_π_3B+/Camera/IMX708.md)

#### BNO085 IMU 
An Inertial Measurement Unit, to track the vehicles movements. This is escential to know which way the robot is pointing at relative to its starting position.

#### URM37 ultrasonic sensor
A sensor capable of detecting how far an object is when its interrupting its signal.


After starting a match we used tthe camera to make various mask with the video.


#### White blob mask
[]()
After aplying a greyscale mask on the image, we made pixels over 40 in brightness white on the mask, and everything else as black, this made a mask that extracted the white from the mat.

#### contours

On the White 
from picamera2 import Picamera2
import cv2
import numpy as np
import math
import CytronComunication
import MainConfiguration
import time


picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={
        "size": (2304, 1296),
        "format": "BGR888"
    },
    sensor={
        "output_size": (2304, 1296)
    },
    buffer_count=1
)

picam2.configure(config)

picam2.start()

time.sleep(1)


distance = None
target_angle = None
steer = 0


while True:

    # Full-resolution camera image
    frame = picam2.capture_array()

    # Make a smaller copy ONLY for displaying
    display = cv2.resize(frame, (640, 360))

    cv2.imshow("Camera", display)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


picam2.stop()
cv2.destroyAllWindows()
from picamera2 import Picamera2
import cv2
import numpy as np
import time

picam2 = Picamera2()

picam2.configure(
    picam2.create_preview_configuration(
        main={
            "size": (2304, 1296),
            "format": "RGB888"
        }
    )
)

picam2.start()
time.sleep(2)

while True:

    # =========================
    # CAMERA
    # =========================

    frame = picam2.capture_array()

    frame = cv2.rotate(
        frame,
        cv2.ROTATE_180
    )

    # =========================
    # RGB -> HSV
    # =========================

    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_RGB2HSV
    )

    # =========================
    # LINE MASK
    # =========================

    lower = np.array([
        105,   # H minimum
        70,   # S minimum
        70    # V minimum
    ])

    upper = np.array([
        120,   # H maximum
        200,   # S maximum
        200    # V maximum
    ])

    mask = cv2.inRange(
        hsv,
        lower,
        upper
    )

    # =========================
    # DISPLAY MASK
    # =========================

    display = cv2.resize(
        mask,
        (640, 360)
    )

    cv2.imshow(
        "Line Mask",
        display
    )

    # =========================
    # QUIT
    # =========================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

picam2.stop()
cv2.destroyAllWindows()

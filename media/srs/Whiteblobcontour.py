from picamera2 import Picamera2
import cv2
import numpy as np
import math
import time


picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={
        "size": (2304, 1296),
        "format": "RGB888"
    },
    sensor={
        "output_size": (2304, 1296)
    },
    buffer_count=1
)

picam2.configure(config)
picam2.start()

time.sleep(1)


threshold = 40

while True:

    # =========================
    # CAMERA
    # =========================

    frame = picam2.capture_array()

    # Rotate 180 degrees
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    # =========================
    # GRAYSCALE
    # =========================

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_RGB2GRAY
    )

    # =========================
    # BINARY
    # =========================

    _, binary = cv2.threshold(
        gray,
        threshold,
        255,
        cv2.THRESH_BINARY
    )

    # =========================
    # BIGGEST WHITE BLOB
    # =========================

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    filtered_binary = np.zeros_like(binary)

    if contours:

        biggest = max(
            contours,
            key=cv2.contourArea
        )

        # Fill biggest blob
        cv2.drawContours(
            filtered_binary,
            [biggest],
            -1,
            255,
            thickness=cv2.FILLED
        )

        # =========================
        # CLEAN CONTOUR
        # =========================

        contour_image = np.zeros_like(binary)

        cv2.drawContours(
            contour_image,
            [biggest],
            -1,
            255,
            thickness=3
        )

    else:

        contour_image = np.zeros_like(binary)

    # =========================
    # DISPLAY
    # =========================

    filtered_display = cv2.resize(
        filtered_binary,
        (640, 360)
    )

    contour_display = cv2.resize(
        contour_image,
        (640, 360)
    )

    cv2.imshow(
        "Biggest White Blob",
        filtered_display
    )

    cv2.imshow(
        "Contour",
        contour_display
    )

    # =========================
    # QUIT
    # =========================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


picam2.stop()
cv2.destroyAllWindows()
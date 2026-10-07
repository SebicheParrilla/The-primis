from picamera2 import Picamera2
import cv2
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

current_frame = None


def mouse_callback(event, x, y, flags, param):
    global current_frame

    if event == cv2.EVENT_MOUSEMOVE and current_frame is not None:

        # RGB pixel
        r, g, b = current_frame[y, x]

        # Convert pixel RGB -> HSV
        pixel = current_frame[y:y+1, x:x+1]
        hsv_pixel = cv2.cvtColor(pixel, cv2.COLOR_RGB2HSV)

        h, s, v = hsv_pixel[0, 0]

        print(f"RGB: ({r}, {g}, {b})    HSV: ({h}, {s}, {v})")


cv2.namedWindow("Camera")
cv2.setMouseCallback("Camera", mouse_callback)


while True:

    frame = picam2.capture_array()

    # Rotate 180°
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    # Display at 640x360
    current_frame = cv2.resize(frame, (640, 360))

    cv2.imshow("Camera", current_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


picam2.stop()
cv2.destroyAllWindows()

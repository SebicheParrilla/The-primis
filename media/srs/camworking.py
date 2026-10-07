from picamera2 import Picamera2
import cv2
import time

picam2 = Picamera2()

picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
)

picam2.start()

time.sleep(2)

while True:
    frame = picam2.capture_array()

    cv2.imshow("Arducam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
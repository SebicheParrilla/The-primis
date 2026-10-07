## First Camera Code
> Retrospective log from July 13, 2026: This entry's information was digitized from the physical engineering notebook.


The first camera program developed for the Raspberry Pi was [camworking.py](../../../code/srs/camworking.py).

```python
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
```

This code captured the frames from the [OV5647](../../../hardware\electrical\Camera\OV5647.md),  and displayed them in a preview.


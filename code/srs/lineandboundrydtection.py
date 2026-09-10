from picamera2 import Picamera2
import cv2
import numpy as np
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

    frame = picam2.capture_array()

    frame = cv2.rotate(
        frame,
        cv2.ROTATE_180
    )

    # --------------------------------
    # WHITE / BLACK DETECTION
    # --------------------------------

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_RGB2GRAY
    )

    _, binary = cv2.threshold(
        gray,
        threshold,
        255,
        cv2.THRESH_BINARY
    )

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    output = np.zeros_like(gray)

    if contours:

        biggest_blob = max(
            contours,
            key=cv2.contourArea
        )

        # --------------------------------
        # BIGGEST WHITE BLOB MASK
        # --------------------------------

        blob_mask = np.zeros_like(gray)

        cv2.drawContours(
            blob_mask,
            [biggest_blob],
            -1,
            255,
            cv2.FILLED
        )

        # --------------------------------
        # FILTERED RAW CAMERA
        # --------------------------------

        filtered_raw = cv2.bitwise_and(
            frame,
            frame,
            mask=blob_mask
        )

        # --------------------------------
        # ORANGE LINE DETECTION
        # FROM FILTERED RAW CAMERA
        # --------------------------------

        filtered_hsv = cv2.cvtColor(
            filtered_raw,
            cv2.COLOR_RGB2HSV
        )

        lower_orange = np.array([
            96,
            111,
            72
        ])

        upper_orange = np.array([
            126,
            203,
            179
        ])

        orange_mask = cv2.inRange(
            filtered_hsv,
            lower_orange,
            upper_orange
        )

        # Dilate orange line
        kernel = np.ones(
            (3, 3),
            np.uint8
        )

        orange_mask = cv2.dilate(
            orange_mask,
            kernel,
            iterations=1
        )

        # --------------------------------
        # USEFUL BLACK → WHITE BOUNDARY
        # --------------------------------

        useful_points = []

        for i, point in enumerate(biggest_blob):

            x, y = point[0]

            if (
                x <= 0 or
                x >= binary.shape[1] - 1 or
                y <= 0 or
                y >= binary.shape[0] - 1
            ):
                continue

            neighborhood = binary[
                y - 1:y + 2,
                x - 1:x + 2
            ]

            if np.any(neighborhood == 0):

                useful_points.append(
                    (i, x, y)
                )

        # --------------------------------
        # SPLIT INTO SECTIONS
        # --------------------------------

        sections = []

        if useful_points:

            current_section = [
                useful_points[0]
            ]

            for j in range(1, len(useful_points)):

                previous_index = useful_points[j - 1][0]
                current_index = useful_points[j][0]

                if current_index == previous_index + 1:

                    current_section.append(
                        useful_points[j]
                    )

                else:

                    sections.append(
                        current_section
                    )

                    current_section = [
                        useful_points[j]
                    ]

            sections.append(
                current_section
            )

        # --------------------------------
        # DRAW USEFUL BOUNDARY
        # --------------------------------

        useful_boundary = np.zeros_like(gray)

        for section in sections:

            for _, x, y in section:

                useful_boundary[y, x] = 255

        boundary_display = cv2.dilate(
            useful_boundary,
            np.ones((3, 3), np.uint8),
            iterations=1
        )

        # --------------------------------
        # FIT LINES
        # --------------------------------

        for section in sections:

            if len(section) < 2:
                continue

            points = np.array(
                [
                    [x, y]
                    for _, x, y in section
                ],
                dtype=np.int32
            ).reshape(-1, 1, 2)

            perimeter = cv2.arcLength(
                points,
                False
            )

            epsilon = 0.007 * perimeter

            corners = cv2.approxPolyDP(
                points,
                epsilon,
                False
            )

            for i in range(
                len(corners) - 1
            ):

                corner1 = tuple(
                    corners[i][0]
                )

                corner2 = tuple(
                    corners[i + 1][0]
                )

                distances1 = np.sum(
                    (
                        points[:, 0, :] -
                        corner1
                    ) ** 2,
                    axis=1
                )

                distances2 = np.sum(
                    (
                        points[:, 0, :] -
                        corner2
                    ) ** 2,
                    axis=1
                )

                index1 = np.argmin(
                    distances1
                )

                index2 = np.argmin(
                    distances2
                )

                if index1 <= index2:

                    line_points = points[
                        index1:index2 + 1
                    ]

                else:

                    line_points = np.concatenate(
                        (
                            points[index1:],
                            points[:index2 + 1]
                        )
                    )

                if len(line_points) < 2:
                    continue

                vx, vy, x0, y0 = cv2.fitLine(
                    line_points,
                    cv2.DIST_L2,
                    0,
                    0.01,
                    0.01
                )

                vx = float(vx)
                vy = float(vy)
                x0 = float(x0)
                y0 = float(y0)

                x1, y1 = corner1
                x2, y2 = corner2

                t1 = (
                    (x1 - x0) * vx +
                    (y1 - y0) * vy
                )

                t2 = (
                    (x2 - x0) * vx +
                    (y2 - y0) * vy
                )

                fit_x1 = int(
                    x0 + t1 * vx
                )

                fit_y1 = int(
                    y0 + t1 * vy
                )

                fit_x2 = int(
                    x0 + t2 * vx
                )

                fit_y2 = int(
                    y0 + t2 * vy
                )

                cv2.line(
                    output,
                    (fit_x1, fit_y1),
                    (fit_x2, fit_y2),
                    255,
                    3
                )

                cv2.circle(
                    output,
                    corner1,
                    6,
                    255,
                    -1
                )

                cv2.circle(
                    output,
                    corner2,
                    6,
                    255,
                    -1
                )

    else:

        filtered_raw = np.zeros_like(frame)
        orange_mask = np.zeros_like(gray)
        boundary_display = np.zeros_like(gray)

    # --------------------------------
    # DISPLAY
    # --------------------------------

    cv2.imshow(
        "Raw Camera",
        cv2.resize(
            frame,
            (640, 360)
        )
    )

    cv2.imshow(
        "Filtered Raw Camera",
        cv2.resize(
            filtered_raw,
            (640, 360)
        )
    )

    cv2.imshow(
        "Orange Line Mask",
        cv2.resize(
            orange_mask,
            (640, 360)
        )
    )

    cv2.imshow(
        "White Blob Mask",
        cv2.resize(
            blob_mask if contours else np.zeros_like(gray),
            (640, 360)
        )
    )

    cv2.imshow(
        "Useful Boundary + FitLines",
        cv2.resize(
            output,
            (640, 360)
        )
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

picam2.stop()
cv2.destroyAllWindows()
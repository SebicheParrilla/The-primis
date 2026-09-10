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

    # =========================
    # CAMERA
    # =========================

    frame = picam2.capture_array()

    frame = cv2.rotate(
        frame,
        cv2.ROTATE_180
    )

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
    # FIND WHITE BLOBS
    # =========================

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    # Empty displays
    blob_mask = np.zeros_like(binary)
    useful_boundary = np.zeros_like(binary)

    if contours:

        # =========================
        # KEEP BIGGEST WHITE BLOB
        # =========================

        biggest_blob = max(
            contours,
            key=cv2.contourArea
        )

        # =========================
        # CREATE WHITE BLOB MASK
        # =========================

        cv2.drawContours(
            blob_mask,
            [biggest_blob],
            -1,
            255,
            -1
        )

        # =========================
        # FILTER BLOB CONTOUR
        #
        # KEEP ONLY CONTOUR PIXELS
        # THAT HAVE A BLACK NEIGHBOR
        # =========================

        useful_points = []

        height, width = binary.shape

        for i, point in enumerate(biggest_blob):

            x, y = point[0]

            # Ignore pixels at camera edge
            if x <= 0 or x >= width - 1:
                continue

            if y <= 0 or y >= height - 1:
                continue

            # 3x3 neighborhood
            neighborhood = binary[
                y - 1:y + 2,
                x - 1:x + 2
            ]

            # Keep contour pixel if ANY
            # neighboring pixel is black
            if np.any(neighborhood == 0):

                useful_points.append(
                    (i, x, y)
                )

        # =========================
        # SPLIT USEFUL POINTS
        # INTO CONTINUOUS SECTIONS
        # =========================

        sections = []
        current_section = []

        for point in useful_points:

            index, x, y = point

            if current_section:

                previous_index = current_section[-1][0]

                # A gap in the original contour
                # means a new useful section
                if index != previous_index + 1:

                    sections.append(
                        current_section
                    )

                    current_section = []

            current_section.append(point)

        # Add final section
        if current_section:

            sections.append(
                current_section
            )

        # =========================
        # DRAW USEFUL PIXELS
        # =========================

        for section in sections:

            for index, x, y in section:

                useful_boundary[y, x] = 255

        # =========================
        # DILATE KEPT PIXELS
        # =========================

        kernel = np.ones(
            (3, 3),
            np.uint8
        )

        useful_boundary = cv2.dilate(
            useful_boundary,
            kernel,
            iterations=1
        )

        # =========================
        # PROCESS EACH SECTION
        # SEPARATELY
        # =========================

        for section in sections:

            if len(section) < 2:
                continue

            # Get just x,y coordinates
            points = np.array(
                [
                    [x, y]
                    for index, x, y in section
                ],
                dtype=np.int32
            ).reshape(-1, 1, 2)

            # =========================
            # FIND CORNERS FOR THIS
            # SECTION ONLY
            # =========================

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

            # =========================
            # FIT LINE BETWEEN
            # EACH PAIR OF CORNERS
            # =========================

            for i in range(len(corners) - 1):

                corner1 = tuple(
                    corners[i][0]
                )

                corner2 = tuple(
                    corners[i + 1][0]
                )

                x1, y1 = corner1
                x2, y2 = corner2

                # =========================
                # FIND POINTS BETWEEN
                # THE TWO CORNERS
                # =========================

                distances1 = np.sum(
                    (points[:, 0, :] -
                     corner1) ** 2,
                    axis=1
                )

                distances2 = np.sum(
                    (points[:, 0, :] -
                     corner2) ** 2,
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

                    line_points = points[
                        index2:index1 + 1
                    ]

                if len(line_points) < 2:
                    continue

                # =========================
                # FIT LINE
                # =========================

                [vx, vy, x0, y0] = cv2.fitLine(
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

                # =========================
                # PROJECT CORNERS
                # ONTO FITTED LINE
                # =========================

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

                # =========================
                # DRAW FITTED LINE
                # =========================

                cv2.line(
                    useful_boundary,
                    (fit_x1, fit_y1),
                    (fit_x2, fit_y2),
                    255,
                    3
                )

            # =========================
            # DRAW CORNERS
            # =========================

            for corner in corners:

                x, y = corner[0]

                cv2.circle(
                    useful_boundary,
                    (x, y),
                    12,
                    255,
                    -1
                )

    # =========================
    # DISPLAY RAW CAMERA
    # =========================

    raw_display = cv2.resize(
        frame,
        (640, 360)
    )

    cv2.imshow(
        "Raw Camera",
        raw_display
    )

    # =========================
    # DISPLAY WHITE BLOB MASK
    # =========================

    blob_display = cv2.resize(
        blob_mask,
        (640, 360)
    )

    cv2.imshow(
        "White Blob Mask",
        blob_display
    )

    # =========================
    # DISPLAY USEFUL BOUNDARY
    # =========================

    boundary_display = cv2.resize(
        useful_boundary,
        (640, 360)
    )

    cv2.imshow(
        "Useful Boundary + FitLines",
        boundary_display
    )

    # =========================
    # QUIT
    # =========================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

picam2.stop()
cv2.destroyAllWindows()
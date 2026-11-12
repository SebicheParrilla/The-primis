from picamera2 import Picamera2
import cv2
import numpy as np
import time
import serial
import threading


# SET TO FALSE WHEN DOING A HEADLESS RUN!
# DEBUG_MODE = True
DEBUG_MODE = False



uart = serial.Serial(
    "/dev/serial0",
    baudrate=115200,
    timeout=0
)

global line_color, line_length
global start 
global servo 
global speed 
start = 1
servo = 0
speed = 3

imu_yaw = 0.0
distance_cm = 0
rx_buffer = ""


line_color = None
line_length = 0
turn_state = "WAIT_DISTANCE"
turn_start_yaw = 0.0

DISTANCE_TRIGGER_CM = 35
TURN_SERVO = 50
TURN_SPEED = 25

cytron_started = False
collision_color = None
line_length = 0

# CAMERA SETUP
picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={
        "size": (640, 360),
        "format": "RGB888"
    },
    sensor={
        "output_size": (2304, 1296)
    },
    buffer_count=1
)

picam2.configure(config)
picam2.start()

time.sleep(0.05)

# Black pixel threshold
threshold = 46




def send_command():

    if cytron_started:

        limited_servo = max(-45, min(45, servo))

        message = f"{start},{limited_servo},{speed}\n"

    else:

        message = f"{start},0,3\n"

    uart.write(message.encode("utf-8"))

def receive_command():

    global cytron_started
    global imu_yaw
    global distance_cm

    if uart.in_waiting:

        data = uart.read(uart.in_waiting)

        if data:

            message = data.decode(
                "utf-8",
                "ignore"
            )

#             print(
#                 message,
#                 end=""
#             )

            messages = message.split("\n")

            for msg in messages:

                msg = msg.strip()

                if not msg:
                    continue

                parts = msg.split(",")

                if len(parts) >= 3:

                    try:

                        startc = int(parts[0])
                        imu_yaw = float(parts[1])
                        distance_cm = int(parts[2])

                        if startc == 1:

                            cytron_started = True

                    except ValueError:

                        print(
                            "Invalid packet:",
                            msg
                        )
        

TX_PERIOD = 0.02
tx_stop = threading.Event()

def uart_communication():

    while not tx_stop.is_set():

        receive_command()
        send_command()
        
#         print("sent")
        
        time.sleep(0.02)




        
# CAMERA PROCESSING
def process_camera():
    
    global collision_color
    global line_length
    
    collision_color = None
    line_length = 0


    # CAPTURE CAMERA
    frame = picam2.capture_array()

    frame = cv2.rotate(
        frame,
        cv2.ROTATE_180
    )


    # WHITE / BLACK DETECTION
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

    # Default values so they always exist
    filtered_raw = np.zeros_like(frame)
    orange_mask = np.zeros_like(gray)
    blue_mask = np.zeros_like(gray)
    boundary_display = np.zeros_like(gray)
    blob_mask = np.zeros_like(gray)

    if contours:

        biggest_blob = max(
            contours,
            key=cv2.contourArea
        )


        # BIGGEST WHITE BLOB MASK
        blob_mask = np.zeros_like(gray)

        cv2.drawContours(
            blob_mask,
            [biggest_blob],
            -1,
            255,
            cv2.FILLED
        )


        # FILTERED RAW CAMERA
        filtered_raw = cv2.bitwise_and(
            frame,
            frame,
            mask=blob_mask
        )


        # ORANGE LINE DETECTION
        filtered_hsv = cv2.cvtColor(
            filtered_raw,
            cv2.COLOR_RGB2HSV
        )

        lower_orange = np.array([
            105,
            35,
            55
        ])

        upper_orange = np.array([
            124,
            220,
            220
        ])

        orange_mask = cv2.inRange(
            filtered_hsv,
            lower_orange,
            upper_orange
        )

        kernel = np.ones(
            (3, 3),
            np.uint8
        )

        orange_mask = cv2.dilate(
            orange_mask,
            kernel,
            iterations=1
        )
        
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            orange_mask,
            connectivity=8
        )

        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            orange_mask,
            connectivity=8
        )

        if num_labels > 1:

            areas = stats[1:, cv2.CC_STAT_AREA]

            biggest_two = np.argsort(areas)[-4:] + 1

            display_mask = np.zeros_like(orange_mask)

            for label in biggest_two:
                display_mask[labels == label] = 255

            orange_mask = display_mask


        # BLUE LINE DETECTION
        blue_lower = np.array([
            0,
            35,
            30
        ])

        blue_upper = np.array([
            12,
            195,
            185
        ])

        blue_mask = cv2.inRange(
            filtered_hsv,
            blue_lower,
            blue_upper
        )

        blue_mask = cv2.dilate(
            blue_mask,
            np.ones((3, 3), np.uint8),
            iterations=1
        )
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            blue_mask,
            connectivity=8
        )
        height, width = orange_mask.shape

        center_x = width // 2

        collision_y = None
        collision_color = None
        start_point = (center_x,height - 1)
    
        end_point = (
            center_x,
            collision_y
        )

        if num_labels > 1:

            areas = stats[1:, cv2.CC_STAT_AREA]

            biggest_two = np.argsort(areas)[-4:] + 1

            display_mask = np.zeros_like(blue_mask)

            for label in biggest_two:
                display_mask[labels == label] = 255

                blue_mask = display_mask
            
        for y in range(height - 1, -1, -1):

            orange_count = np.count_nonzero(
            orange_mask[max(0, y - 2):y + 3, center_x]
            )

            blue_count = np.count_nonzero(
                blue_mask[max(0, y - 2):y + 3, center_x]
            )
            

            if orange_count >= 3:
                collision_y = y
                line_length = (height - 1) - collision_y
                collision_color = "orange"
#                 print("orange", line_length)
                
                break

            if blue_count >= 3:
                collision_y = y
                line_length = (height - 1) - collision_y
                collision_color = "blue"
#                 print("blue",line_length)
                
                break
            
            if orange_mask[y, center_x] > 0:
                line_color = "orange"
                line_length = (height - 1) - y
                
                break

            if blue_mask[y, center_x] > 0:
                line_color = "blue"
                line_length = (height - 1) - y
                
                break
            


        # ADD COLORED LINES TO ORIGINAL BLOB
        line_mask = cv2.bitwise_or(
            orange_mask,
            blue_mask
        )
        
    


        blob_mask[line_mask > 0] = 255


        # USEFUL BLACK → WHITE BOUNDARY
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


        # SPLIT INTO SECTIONS
        sections = []

        if useful_points:

            current_section = [
                useful_points[0]
            ]

            for j in range(
                1,
                len(useful_points)
            ):

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


        # DRAW USEFUL BOUNDARY
        useful_boundary = np.zeros_like(gray)

        for section in sections:

            for _, x, y in section:

                useful_boundary[y, x] = 255

        boundary_display = cv2.dilate(
            useful_boundary,
            np.ones((3, 3), np.uint8),
            iterations=1
        )


        # FIT LINES
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
                
                


    # DISPLAY
    if DEBUG_MODE:

#         cv2.imshow(
#             "White Blob Mask",
#             cv2.resize(
#                 blob_mask,
#                 (640, 360)
#             )
#         )



#         cv2.imshow(
#             "Useful Boundary + FitLines",
#             cv2.resize(
#                 output,
#                 (640, 360)
#             )
#         )


        # ALL MASKS ON FILTERED RAW
        overlay = filtered_raw.copy()

        # Blue line
        overlay[blue_mask > 0] = [255, 0, 0]

        # Orange line
        overlay[orange_mask > 0] = [0, 140, 255]

        # Boundaries
        overlay[boundary_display > 0] = [0, 0, 255]

        cv2.imshow(
            "Filtered Raw + Masks",
            cv2.resize(
                overlay,
                (640, 360)
            )
        )
        
        cv2.imshow(
             "blue_mask",
             cv2.resize(
                 blue_mask,
                 (640, 360)
            )
        )
#          cv2.imshow(
#              "Filtered Raw + Masks",
#              cv2.resize(
#                  overlay,
#                  (640, 360)
#              )
#          )


        cv2.waitKey(1)


# PI BOOT
print("WAITING FOR CYTRON START")

threading.Thread(
    target=uart_communication,
    daemon=True
).start()



# WAIT FOR CYTRON
while not cytron_started:
    # PROCESS CAMERA
    process_camera()
    


    time.sleep(0.01)

# AUTONOMOUS CAMERA LOOP
print("AUTONOMOUS PROGRAM STARTED")

last_command_time = time.monotonic()

first_line_color = None

turn_count = 0

while True:

    process_camera()

    if cytron_started:
        time.sleep(0.3)
#         print("started")


        # -------------------------
        # FIND FIRST LINE
        # -------------------------
        if collision_color is None:

            process_camera()
            speed = 4
            

        if first_line_color is None and collision_color is not None:
            first_line_color = collision_color
            print("FIRST LINE:", first_line_color)

        # -------------------------
        # WAIT FOR LINE <= 100
        # -------------------------
        

        if first_line_color is not None:
            
            for _ in range(12):
                
                turn_count += 1
                print("TURN COUNT:", turn_count)

                turn_start_yaw = imu_yaw

                if first_line_color == "orange":
                    target_yaw = turn_start_yaw - 90
                    if target_yaw < 180:
                        target_yaw += 360

                elif first_line_color == "blue":
                    target_yaw = turn_start_yaw + 90
                    if target_yaw > 180:
                        target_yaw -= 360

                while True:
                    process_camera()
                    print(
                        "START:",
                        turn_start_yaw,
                        "line_length:",
                        line_length,
                        "color:",
                        first_line_color,
                        "TARGET:",
                        target_yaw,
                        "CURRENT:",
                        imu_yaw
                    )

                        
                    speed = 5
                        
                        
                    if 0 < line_length < 25:
                            
                        if first_line_color == "orange":
                            servo = 41

                        elif first_line_color == "blue":
                            servo = -41
                                                                    
                    if first_line_color == "orange" and imu_yaw <= target_yaw:
                        servo = 0
                        break
                                    
                    if first_line_color == "blue" and imu_yaw >= target_yaw:
                        servo = 0
                        break
                    
            break
                                
                        
    time.sleep(0.001)


# CLEANUP
tx_stop.set()
uart.close()

picam2.stop()
cv2.destroyAllWindows()




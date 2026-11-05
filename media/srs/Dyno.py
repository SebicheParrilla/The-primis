
from machine import Pin
import time
import math

# ==================================================
# TEST SETTINGS
# ==================================================

PRESSURE_PSI = 20

SLOTS = 16
TIMEOUT_US = 300000

CALIBRATION_WEIGHT_G = 26.0

# Mechanical transmission:
# Engine rotates 3 times for every dyno rotation
DRIVE_RATIO = 3.0

# Effective perpendicular torque arm
TORQUE_ARM_M = 0.1

# Nm * RPM / this constant = mechanical HP
HP_CONSTANT = 7121.0


# ==================================================
# PIN CONFIGURATION
# ==================================================

dt = Pin(26, Pin.IN, Pin.PULL_UP)
sck = Pin(27, Pin.OUT, value=0)

sensor = Pin(7, Pin.IN)

# Solenoid active LOW
solenoid = Pin(0, Pin.OUT)
solenoid.value(1)

button = Pin(20, Pin.IN, Pin.PULL_UP)


# ==================================================
# OPTICAL ENCODER
# ==================================================

flywheel_count = 0

last_state = sensor.value()
last_count_time = time.ticks_us()

intervals = []


def add_sample(value):

    intervals.append(value)

    if len(intervals) > 7:
        intervals.pop(0)


def update_encoder():

    global flywheel_count
    global last_state
    global last_count_time

    current_time = time.ticks_us()
    current_state = sensor.value()

    if last_state == 0 and current_state == 1:

        elapsed = time.ticks_diff(
            current_time,
            last_count_time
        )

        flywheel_count += 1
        last_count_time = current_time

        add_sample(elapsed)

    # Detect stopped flywheel
    if time.ticks_diff(
        current_time,
        last_count_time
    ) >= TIMEOUT_US:

        if not intervals or intervals[-1] != 0:
            add_sample(0)

    last_state = current_state


def get_rpm():

    if not intervals:
        return 0

    if intervals[-1] == 0:
        return 0

    valid = [x for x in intervals if x > 0]

    if not valid:
        return 0

    average = sum(valid) / len(valid)

    return 60000000 / (average * SLOTS)


def reset_encoder():

    global flywheel_count
    global last_state
    global last_count_time

    flywheel_count = 0
    intervals.clear()

    last_state = sensor.value()
    last_count_time = time.ticks_us()


# ==================================================
# HX711
# ==================================================

def read_hx711():

    start = time.ticks_ms()

    # Wait for conversion ready.
    # Keep polling the optical encoder while waiting.
    while dt.value() == 1:

        update_encoder()

        if time.ticks_diff(
            time.ticks_ms(), start
        ) > 1000:

            return None

        time.sleep_us(10)

    value = 0

    # Read 24 bits
    for _ in range(24):

        sck.value(1)
        time.sleep_us(1)

        value = (value << 1) | dt.value()

        sck.value(0)
        time.sleep_us(1)

    # 25th pulse: Channel A, gain 128
    sck.value(1)
    time.sleep_us(1)
    sck.value(0)

    # Signed 24-bit conversion
    if value & 0x800000:
        value -= 0x1000000

    return value


def average_readings(samples=10):

    values = []

    while len(values) < samples:

        reading = read_hx711()

        if reading is not None:
            values.append(reading)

    return sum(values) / len(values)


# ==================================================
# BUTTON
# ==================================================

def button_pressed():

    if button.value() == 0:

        time.sleep_ms(30)

        if button.value() == 0:

            while button.value() == 0:
                time.sleep_ms(10)

            return True

    return False


def wait_for_button(message):

    print("\n" + message)

    while True:

        if button_pressed():
            return

        time.sleep_ms(10)


# ==================================================
# DYNO CALCULATIONS
# ==================================================

def calculate_results(raw, caliper_zero, counts_per_gram, rpm):

    # Convert raw counts to grams of reaction force
    force_g = abs(raw - caliper_zero) / counts_per_gram

    # Convert grams to Newtons
    force_N = (force_g / 1000.0) * 9.81

    # Torque measured at the dyno
    dyno_torque = force_N * TORQUE_ARM_M

    # Convert dyno torque to estimated engine torque
    engine_torque = dyno_torque / DRIVE_RATIO

    # Calculate engine horsepower using engine RPM
    hp = (engine_torque * rpm) / HP_CONSTANT

    return force_g, force_N, dyno_torque, engine_torque, hp


# ==================================================
# INITIALIZATION
# ==================================================

print("================================")
print("         PNEUMATIC DYNO")
print("================================")

print("Pressure:", PRESSURE_PSI, "PSI")
print("Transmission ratio:", DRIVE_RATIO, ":1")
print("Torque arm:", TORQUE_ARM_M * 1000, "mm")

print("\nSOLENOID OFF")


# ==================================================
# CALIBRATION SEQUENCE
# ==================================================

# STEP 1: ZERO WITHOUT CALIPER

wait_for_button(
    "STEP 1: Leave load cell unloaded.\n"
    "Press button to capture zero."
)

print("Capturing unloaded zero...")

zero_offset = average_readings(10)

print("Unloaded zero:", zero_offset)


# STEP 2: CALIBRATION WEIGHT

wait_for_button(
    "STEP 2: Place the 26g calibration weight.\n"
    "Press button when weight is in position."
)

print("Measuring calibration weight...")

loaded_reading = average_readings(10)

counts_per_gram = abs(
    loaded_reading - zero_offset
) / CALIBRATION_WEIGHT_G

print("\nCALIBRATION RESULTS")
print("Zero:", zero_offset)
print("Loaded:", loaded_reading)
print("Counts per gram:", counts_per_gram)

if counts_per_gram < 1:
    print("ERROR: Invalid calibration!")
    raise Exception("Calibration failed")


# STEP 3: CALIPER TARE AND START

wait_for_button(
    "STEP 3: Remove the 26g weight.\n"
    "Install the caliper in its testing position.\n"
    "Press button to tare the caliper and START."
)

print("Capturing caliper baseline...")

caliper_zero = average_readings(10)

print("Caliper zero:", caliper_zero)

# Reset encoder before engine starts
reset_encoder()

max_rpm = 0

max_force_g = 0
max_dyno_torque = 0
max_engine_torque = 0
max_torque_rpm = 0

max_hp = 0
max_hp_rpm = 0

start_time = 0

print("\nSOLENOID ON")
solenoid.value(0)


# ==================================================
# WAIT FOR ENGINE RPM
# ==================================================

print("Waiting for engine RPM...")

while True:

    update_encoder()
    rpm = get_rpm()

    if rpm > 0:

        start_time = time.ticks_ms()
        max_rpm = rpm

        print("ENGINE STARTED!")
        break

    time.sleep_ms(1)


# ==================================================
# RUNNING TEST
# ==================================================

print("\nTEST RUNNING - APPLY BRAKE")
print("--------------------------------")

while True:

    # Read HX711 while continuing encoder polling
    raw = read_hx711()

    update_encoder()
    rpm = get_rpm()

    if raw is None:
        continue

    elapsed = time.ticks_diff(
        time.ticks_ms(),
        start_time
    ) / 1000.0

    if rpm > max_rpm:
        max_rpm = rpm

    force_g, force_N, dyno_torque, engine_torque, hp = calculate_results(
        raw,
        caliper_zero,
        counts_per_gram,
        rpm
    )

    # Track maximum torque while engine is rotating
    if rpm > 0:

        if engine_torque > max_engine_torque:

            max_force_g = force_g
            max_dyno_torque = dyno_torque
            max_engine_torque = engine_torque
            max_torque_rpm = rpm

        # Track maximum horsepower independently
        if hp > max_hp:

            max_hp = hp
            max_hp_rpm = rpm

    print(
        "RPM: {:.1f} | TIME: {:.1f}s | "
        "FORCE: {:.2f}g | "
        "DYNO T: {:.4f}Nm | "
        "ENGINE T: {:.4f}Nm | "
        "HP: {:.4f}".format(
            rpm,
            elapsed,
            force_g,
            dyno_torque,
            engine_torque,
            hp
        )
    )

    # Flywheel stopped
    if rpm == 0:

        solenoid.value(1)

        print("\n================================")
        print("          TEST RESULTS")
        print("================================")

        print("Pressure:", PRESSURE_PSI, "PSI")
        print("Elapsed time:", elapsed, "seconds")
        print("Maximum RPM:", round(max_rpm, 2))

        print("\nMAXIMUM TORQUE")
        print("Force:", round(max_force_g, 2), "g")
        print("Dyno torque:", round(max_dyno_torque, 4), "Nm")
        print("Estimated engine torque:", round(max_engine_torque, 4), "Nm")
        print("RPM at maximum torque:", round(max_torque_rpm, 2))
        print("Calibration (counts/g):", round(counts_per_gram, 3))

        print("\nMAXIMUM HORSEPOWER")
        print("HP:", round(max_hp, 4))
        print("RPM at maximum HP:", round(max_hp_rpm, 2))

        print("\nSOLENOID OFF")
        print("================================")

        break


# ==================================================
# END
# ==================================================

print("\nTEST COMPLETE")

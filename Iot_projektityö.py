import time
from grove.adc import ADC
from grove.grove_servo import GroveServo


# --- SENSOR LUOKKA ---
class GroveLightSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def light(self):
        return self.adc.read(self.channel)


# --- PINNIT ---
LEFT_SENSOR_CHANNEL = 0   # A0
RIGHT_SENSOR_CHANNEL = 4  # A4
SERVO_PIN = 12            # pwm
# --- ASETUKSET ---
TOLERANCE = 20        # kuinka lähellä arvot pitää olla
SERVO_STEP = 2        # kuinka paljon servo liikkuu
MIN_ANGLE = 0
MAX_ANGLE = 180

# --- INIT ---
left_sensor = GroveLightSensor(LEFT_SENSOR_CHANNEL)
right_sensor = GroveLightSensor(RIGHT_SENSOR_CHANNEL)
servo = GroveServo(SERVO_PIN)

angle = 90
servo.setAngle(angle)

print("Starting light balancing...")

while True:
    left_value = left_sensor.light
    right_value = right_sensor.light

    diff = left_value - right_value

    print(f"Left: {left_value}  Right: {right_value}  Diff: {diff}")

    # jos arvot lähes samat -> ei liikettä
    if abs(diff) <= TOLERANCE:
        print("Balanced")
    else:
        if diff > 0:
            angle -= SERVO_STEP
        else:
            angle += SERVO_STEP

        angle = max(MIN_ANGLE, min(MAX_ANGLE, angle))
        servo.setAngle(angle)
        print(f"Servo angle: {angle}")

    time.sleep(0.2)

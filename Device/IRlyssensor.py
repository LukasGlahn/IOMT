import RPi.GPIO as GPIO #Husk at pip install RPI.GPIO på Raspberry Pi
import time

# Sensor Digital Pin Configuration
pin_sensor_digital = 24  # flammesensor
pin_led = 23  # Powerled

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(pin_sensor_digital, GPIO.IN)  # Flammesensor bliver sat som input
GPIO.setup(pin_led, GPIO.OUT)  # LED bliver sat som output

try:
    # Main loop
    while True:
        sensor_value_digital = GPIO.input(pin_sensor_digital)

        if sensor_value_digital == 1:
            GPIO.output(pin_led, GPIO.HIGH)  # Sluk LED
        else:
            GPIO.output(pin_led, GPIO.LOW)  # Tænd LED
except KeyboardInterrupt:
    print("Kode afsluttet")
finally:
    GPIO.cleanup()  # Nulstiller GPIO states

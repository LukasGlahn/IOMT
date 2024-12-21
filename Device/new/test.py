import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode( GPIO.BCM )
GPIO.setup( 26, GPIO.OUT )



while True:
    sleep(2)
    GPIO.output( 26, GPIO.HIGH )
    print("high")
    sleep(2)
    GPIO.output(26, GPIO.LOW)
    print("low")
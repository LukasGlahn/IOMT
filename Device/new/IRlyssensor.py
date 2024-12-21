import RPi.GPIO as GPIO #Husk at pip install RPI.GPIO på Raspberry Pi
import time


class ir_sensor():

    def __init__(self,pin_sensor, pin_led):
        # Sensor Digital Pin Configuration
        self.pin_sensor_digital = pin_sensor  # flammesensor pin 24
        self.pin_led = pin_led  # Powerled pin 23



    def main(self):
        try:
            # Main loop
                    # GPIO setup
            GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
            GPIO.setup(self.pin_sensor_digital, GPIO.IN)  # Flammesensor bliver sat som input
            GPIO.setup(self.pin_led, GPIO.OUT)  # LED bliver sat som output
            sensor_value_digital = GPIO.input(self.pin_sensor_digital)

            if sensor_value_digital == 1:
                GPIO.output(self.pin_led, GPIO.LOW)  # Sluk LED
                
            else:
                GPIO.output(self.pin_led, GPIO.HIGH)  # Tænd LED
                
        except KeyboardInterrupt:
            print("Kode afsluttet")
            GPIO.cleanup()  # Nulstiller GPIO states
            exit()


#ir = ir_sensor(24,23)

#while True:
#    ir.main()
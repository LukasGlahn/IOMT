import RPi.GPIO as GPIO
import time


class Motore():

    def __init__(self, direction=False, step=0.002, pin1=21, pin2=20, pin3=16, pin4=12):
        self.in1 = pin1
        self.in2 = pin2
        self.in3 = pin3
        self.in4 = pin4

        # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
        self.step_sleep = step

        self.step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°

        self.direction = direction # True for clockwise, False for counter-clockwise

        # defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
        self.step_sequence = [[1,0,0,1],
                        [1,0,0,0],
                        [1,1,0,0],
                        [0,1,0,0],
                        [0,1,1,0],
                        [0,0,1,0],
                        [0,0,1,1],
                        [0,0,0,1]]
    def rotade(self,steps):
        self.step_count = steps # 5.625*(1/64) per step, 4096 steps is 360°
        # setting up
        GPIO.setmode( GPIO.BCM )
        GPIO.setup( self.in1, GPIO.OUT )
        GPIO.setup( self.in2, GPIO.OUT )
        GPIO.setup( self.in3, GPIO.OUT )
        GPIO.setup( self.in4, GPIO.OUT )

        # initializing
        GPIO.output( self.in1, GPIO.LOW )
        GPIO.output( self.in2, GPIO.LOW )
        GPIO.output( self.in3, GPIO.LOW )
        GPIO.output( self.in4, GPIO.LOW )

        motor_pins = [self.in1,self.in2,self.in3,self.in4]
        motor_step_counter = 0 ;

        def cleanup():
            GPIO.output( self.in1, GPIO.LOW )
            GPIO.output( self.in2, GPIO.LOW )
            GPIO.output( self.in3, GPIO.LOW )
            GPIO.output( self.in4, GPIO.LOW )
            GPIO.cleanup()

        # the meat
        try:
            i = 0
            for i in range(self.step_count):
                for pin in range(0, len(motor_pins)):
                    GPIO.output( motor_pins[pin], self.step_sequence[motor_step_counter][pin] )
                if self.direction==True:
                    motor_step_counter = (motor_step_counter - 1) % 8
                elif self.direction==False:
                    motor_step_counter = (motor_step_counter + 1) % 8
                else: # defensive programming
                    print( "uh oh... direction should *always* be either True or False" )
                    cleanup()
                    exit( 1 )
                time.sleep( self.step_sleep )

        except KeyboardInterrupt:
            cleanup()
            exit( 1 )

        cleanup()

#moter = Motore()

#moter.rotade(4000)
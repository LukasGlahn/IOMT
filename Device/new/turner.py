from motor import Motore
import json
from datetime import datetime
import RPi.GPIO as GPIO
from time import sleep
moter = Motore()
#print("begin")


scetuals = []
dd = '["2024-12-16T17:45", [1, "1"]]'

data = json.loads(dd)
#print(data)
if type(data[0]) is str:
    date = data.pop(0)
    date = date.replace("T", " ")
    
    target_datetime = datetime.strptime(date, "%Y-%m-%d %H:%M")
    log = {
        "time":target_datetime,
        "piller":data
        }


def decimal_to_5bit_list(number):
    """
    Funktion der konverterer et base 10 tal (0-31) til en 5-bit binær 
    værdi i en liste, så pilledispenseren kan styres. 

    Argumenter:
        En integer der skal konverteres. Skal være mellem 0 og 31.
    
    Returnerer:
        En liste med en binær værdi. 
    
    Fejlhåndtering:
        'ValueError' hvis tallet ikke er mellem 0 og 31.
    """
    if number < 0 or number > 31:
        raise ValueError("Tallet skal være mellem 0 og 31.")

    # Konverter tallet til binær og fyld op til 5 bit
    binary_str = bin(number)[2:].zfill(5)

    # Lav en liste af binære værdier
    binary_list = [int(digit) for digit in binary_str]

    return binary_list

def bit_lock(row):
    GPIO.setmode( GPIO.BCM )
    GPIO.setup( 5, GPIO.OUT )
    GPIO.setup( 6, GPIO.OUT )
    GPIO.setup( 13, GPIO.OUT )
    GPIO.setup( 19, GPIO.OUT )
    GPIO.setup( 26, GPIO.OUT )
    pins = (26,19,13,6,5)
    i = 0
    for bit in row:
        if bit == 1:
            GPIO.output( pins[i], GPIO.HIGH )
            print(pins[i], "high")
        else:
            GPIO.output(pins[i], GPIO.LOW)
            print(pins[i], "low")
        i += 1


def turn(pills):
    for pill in pills:
        bit_lock(decimal_to_5bit_list(pill[0]))
        moter.rotade(700*int(pill[1]))
        GPIO.cleanup()
        
    
    
#while True:

    
#    turn(log["piller"])
#    sleep(2)


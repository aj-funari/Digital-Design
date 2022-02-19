import smbus
import sys
import time
import numpy as np
import pigpio

class Basys3_LEDSW:
    def __init__(self):
        self.pi = pigpio.pi()
        self.pi.set_mode(10,pigpio.OUTPUT)
        self.pi.set_mode(11,pigpio.OUTPUT)
        self.pi.set_mode(8,pigpio.OUTPUT)
        self.pi.set_mode(9,pigpio.INPUT)


    def write_led(self, led_num):
        #led_num is between 0 and 7 and reps LED[0] - LED[7] on B3 board
        #Only one LED on at a time
        #Function will return no value
        #going from 0-7 in binary, led_num ==0 then 000 etc..
        if (led_num == 0 ):
            self.pi.write(10, 0)
            self.pi.write(11, 0)
            self.pi.write(8,0)
        if (led_num == 1 ):
            self.pi.write(10, 1)
            self.pi.write(11, 0)
            self.pi.write(8,0)
        if (led_num == 2 ):
            self.pi.write(10, 0)
            self.pi.write(11, 1)
            self.pi.write(8,0)
        if (led_num == 3 ):
            self.pi.write(10, 1)
            self.pi.write(11, 1)
            self.pi.write(8,0)
        if (led_num == 4 ):
            self.pi.write(10, 0)
            self.pi.write(11, 0)
            self.pi.write(8,1)
        if (led_num == 5 ):
            self.pi.write(10, 1)
            self.pi.write(11, 0)
            self.pi.write(8,1)
        if (led_num == 6 ):
            self.pi.write(10, 0)
            self.pi.write(11, 1)
            self.pi.write(8,1)
        if (led_num == 7 ):
            self.pi.write(10, 1)
            self.pi.write(11, 1)
            self.pi.write(8,1)


    def read_switch(self):
        #returns state of SW[0] on B3 board
        #return of 1 means on, and return of 0 means off
        return (self.pi.read(9))



if  __name__ == "__main__": #this will test my function
    foo = Basys3_LEDSW()
    freq = float(input("Enter a freqeuncy between 3Hz and 10Hz : "))
    period = 1/freq
    led = 0
    while(1):
        foo.write_led(led)
        if(foo.read_switch()):
            led = (led + 1) % 8
        else:
            led = (led - 1) % 8
        time.sleep(period)


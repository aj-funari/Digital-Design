import smbus
import sys
import time
import numpy as np
class lps331:
    ''' allows connection from Raspberry pi to I2C connected lps331 '''

    def __init__(self,raspberry_pi_i2c_port=1):
        self.i2c_port_number = raspberry_pi_i2c_port
        self.bus = smbus.SMBus(self.i2c_port_number)
        self.address = self.find_sensor()
        if (self.address == 0):
            print("Error: could not read from sensor at i2c address 0x5d")
            sys.exit()
        self.enable_sensor()

    def find_sensor(self):
        ''' read the whoami byte from i2c address 0x5d and confirm to be 0xbb '''
        # Return the address if found (0x5d) and 0 if not found

        self.bus = smbus.SMBus(1)
        self.data = self.bus.read_byte_data(0x5d, 0x0f)

        if (self.data == 0xbb):
            print("Found Sensor")
            return(self.data)
        else:
            print("Received %d from the sensor " %(self.data))
            return(0)

        return(-1);   # if the sensor was not located on either bus, return -1

        self.bus.close()


    def i2c_address(self):
        return(self.address)

    def sample_once(self):
        ''' Cause the sensor to sample one time '''

        address = 0x5d
        self.ctrl_reg2 = self.bus.read_byte_data(address,0x21)
        self.bus.write_byte_data(address,0x21,0x01|self.ctrl_reg2)
        self.ctrl_reg2 = self.bus.read_byte_data(address,0x21)

        while (self.ctrl_reg2&0x01):
            self.ctrl_reg2 = self.bus.read_byte_data(address, 0x21)
        return

    def read_temperature(self):
        ''' Sample, read temperature registers, and convert to inhg '''
        address = 0x5d
        self.sample_once()
        templ = self.bus.read_byte_data(address, 0x2b)
        temph = self.bus.read_byte_data(address, 0x2c)
        tempC = temph << 8 | templ #h is highest, l is next then xl
        tempC = np.int16(tempC) #n32 for pressure
        tempC = (42.5 + tempC/480)
        return tempC

    def read_pressure(self):
        ''' Sample, read pressure registers, and convert to inhg '''

        #press_inhg = 0
        address = 0x5d
        self.sample_once()
        pressh = self.bus.read_byte_data(address, 0x2a)
        pressl = self.bus.read_byte_data(address, 0x29)
        pressxl = self.bus.read_byte_data(address, 0x28)
        press_inhg = pressh << 16 | pressl << 8 | pressxl
        press_inhg = np.int32(press_inhg)
        press_inhg = (press_inhg/4096)* .033

        return(press_inhg)


    def enable_sensor(self):
        ''' Turn on sensor in control register 1'''
        address = 0x5d

        #using the 7th bit of register 1, enable pressure and temperature, PD=1
        self.ctrl_reg1 = self.bus.read_byte_data(address,0x20)
        self.bus.write_byte_data(address, 0x20, 0x80|self.ctrl_reg1)
        print("Enabled sensor")
                              
    def disable_sensor(self):
        ''' Turn off sensor in control register 1 '''

        address = 0x5d
        self.ctrl_reg1 = self.bus.read_byte_data(address,0x20) #might be self.address
        self.bus.write_byte_data(address, 0x20, 0x80&self.ctrl_reg1)
        print("Disabled sensor")


    def close(self):
        ''' Disable the sensor and close connection to i2c port '''
        self.disable_sensor()
        self.bus.close()

if  __name__ == "__main__":
    sensor = lps331(1)
    print("Temperature = %0.2f Deg C "%(sensor.read_temperature()))
    print("Pressure = %0.2f inHg"%(sensor.read_pressure()))
    sensor.close()

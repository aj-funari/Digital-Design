import paho.mqtt.client as mqtt
import time
import lps331class
import Basys3_LEDSW

# White Bar Code Label Number on Each Raspberry Pi
sensor_id = 986302
temperature = 21
pressure = 31
switch = 0

lps = lps331class.lps331()
bas = Basys3_LEDSW.Basys3_LEDSW()

def on_message(client, userdata, message):
#    print("topic:", message.topic)
#   write to led message.payload.decode('UTF-8')
    print("message:", message.payload.decode('UTF-8'))
    print("Enter number (0-8): ")
    n = str(message.payload.decode('UTF-8'))
    print("number: ",n )
    n = int(n)
    if(n >= 0 and n <= 8):


    #check between 0-8 maybe convert
    #convert  to integer
    else:
        print("not between 0 and 8")
        return(-1)

def on_connect(client,userdata,flags,rc):
    client.subscribe(f"sensors/{sensor_id}/led")

client = mqtt.Client()
client.on_message=on_message
client.on_connect=on_connect
client.connect("pivot.iuiot.org")
client.loop_start()
while(1):
#read from switch, temp and pressure
    switch = bas.read_switch()
    temperature = lps.read_temperature()
    pressure = lps.read_pressure()

    print("Publish Temperature, Pressure, and Switch Data")
    client.publish(f"sensors/{sensor_id}/temperature",f"{temperature}")
    client.publish(f"sensors/{sensor_id}/pressure",f"{pressure}")
    client.publish(f"sensors/{sensor_id}/switch",f"{switch}")
    time.sleep(15)


from battery_status import Battery_Status

#from gps_to_adafruit import *

from time import ticks_ms, sleep

#########################################################################
# CONFIGURATION


#########################################################################
# OBJECTS

Battery = Battery_Status()

#########################################################################
# PROGRAM

battery_status_start = ticks_ms()
battery_status_period_ms = 1000

gps_to_adafruit_start = ticks_ms()
gps_to_adafruit_period_ms = 300

while True:
    #------------------------------------------------------
    # Battery Status
    
    if ticks_ms() - battery_status_start > battery_status_period_ms:
        battery_status_start = ticks_ms()
        
        Battery.battery_status()

    #------------------------------------------------------
    # GPS to Adafruit
    
    
    

from battery_status import Battery_Status
from send_to_adafruit import Send_to_Adafruit
from gps_stuff import GPS_Stuff
from reg_tackling import Reg_Tackling
from reg_inactivity import Reg_Inactivity

import umqtt_robust2 as mqtt
import _thread

from machine import ADC, Pin
from time import ticks_ms, sleep
import sys

#########################################################################
# CONFIGURATION

pin_adc_bat = 32

gps_test_data = 0.346324,55.69168,12.55455,0.0
#########################################################################
# OBJECTS
bat_adc = ADC(Pin(pin_adc_bat, Pin.IN))        # The battery status ADC object
bat_adc.atten(ADC.ATTN_11DB)           # Full range: 3,3 V
#bat_adc.width(ADC.WIDTH_12BIT)         # Bestemmer opløsningen i bits 12 (111111111111 = 4096)


Battery = Battery_Status(bat_adc)
GPS = GPS_Stuff()
Tackling = Reg_Tackling()
Inactivity = Reg_Inactivity(GPS)

Adafruit = Send_to_Adafruit(GPS, mqtt, Tackling, Inactivity)

#########################################################################
# PROGRAM

battery_status_start = ticks_ms()
battery_status_period_ms = 1000 # 1000ms = 1s

send_to_adafruit_start = ticks_ms()
send_to_adafruit_period_ms = 5000 # 10000ms = 10s

gps_stuff_start = ticks_ms()
gps_stuff_period_ms = 1000

tackling_reg_start = ticks_ms()
tackling_reg_period_ms = 1000

inactivity_reg_start = ticks_ms()
inactivity_reg_period_ms = 1000


while True:
    try:
        #------------------------------------------------------
        # Battery Status
        
        if ticks_ms() - battery_status_start > battery_status_period_ms:
            battery_status_start = ticks_ms()
            
            Battery.battery_status()
        
        #------------------------------------------------------
        # GPS Stuff
        
        # if ticks_ms() - gps_stuff_start > gps_stuff_period_ms:
        #     gps_stuff_start = ticks_ms()
            
        #     print(GPS.get_adafruit_gps())
        
        #------------------------------------------------------
        # Register Tackling
        
        if ticks_ms() - tackling_reg_start > tackling_reg_period_ms:
            tackling_reg_start = ticks_ms()
            Tackling.reg_tackling()
        
        #------------------------------------------------------
        # Register Inactivity
        
        if ticks_ms() - inactivity_reg_start > inactivity_reg_period_ms:
            inactivity_reg_start = ticks_ms()
            Inactivity.reg_inactivity()
            
        
        #------------------------------------------------------
        # Send to Adafruit
        
        if ticks_ms() - send_to_adafruit_start > send_to_adafruit_period_ms:
            send_to_adafruit_start = ticks_ms()
            
            #Adafruit.gps_to_adafruit()
            #Adafruit.tackling_to_adafruit()
            #Adafruit.inactivity_to_adafruit()
            
            Adafruit.send_to_adafruit()
    


    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        sys.exit()
        

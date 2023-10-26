from battery_status import Battery_Status

#from gps_bare_minimum import GPS_Minimum
#from gps_to_adafruit import *

from machine import ADC, Pin
from time import ticks_ms, sleep

#########################################################################
# CONFIGURATION

pin_adc_bat = 25 

# Button
pin_adc_button = 4

#########################################################################
# OBJECTS
bat_adc = ADC(Pin(pin_adc_bat))        # The battery status ADC object
bat_adc.atten(ADC.ATTN_11DB)           # Full range: 3,3 V
bat_adc.width(ADC.WIDTH_12BIT)         # Bestemmer opløsningen i bits 12 (111111111111 = 4096)

# Instantierer knap som objekt
pb = Pin(pin_adc_button, Pin.IN)

Battery = Battery_Status(bat_adc, pb)

#########################################################################
# PROGRAM

battery_status_start = ticks_ms()
battery_status_period_ms = 100

while True:
    #------------------------------------------------------
    # Battery Status
    
    if ticks_ms() - battery_status_start > battery_status_period_ms:
        battery_status_start = ticks_ms()
        
        bat_voltage = Battery.read_battery_voltage_avg64()
        bat_percentage = Battery.battery_percentage(bat_voltage)
        # print(bat_adc.read())
        # print(bat_voltage)
        # print(button)

        print("Battery charge percentage:", bat_percentage, "%")

        button = pb.value()

        if button == 1:
            Battery.update_led_ring(bat_percentage)
            print("Updating LED ring")
        else:
            Battery.clear_led_ring()

    #------------------------------------------------------
    
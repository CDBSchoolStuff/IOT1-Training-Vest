import sys, uselect
from machine import UART, Pin, ADC
from time import sleep, sleep_ms

#########################################################################
# CONFIGURATION

# Battery
pin_adc_bat = 25                       # The battery status input pin
max_adc_val = 3420                     # Målt 
bat_scaling = 4.2 / max_adc_val        # The battery voltage divider ratio, replace <adc_4v2> with ADC value when 4,2 V applied

# Voltages
max_pin_voltage = 3.3
max_bat_voltage = 4.2
min_bat_voltage = 3.0

# Resistors
resistor1 = 4.7
resistor2 = 9.92


#########################################################################
# OBJECTS

bat_adc = ADC(Pin(pin_adc_bat))        # The battery status ADC object
bat_adc.atten(ADC.ATTN_11DB)           # Full range: 3,3 V
bat_adc.width(ADC.WIDTH_12BIT)         # Bestemmer opløsningen i bits 12 (111111111111 = 4096)



#########################################################################
# Functions

def calc_spaendingsdeler(U, R1, R2):
    U_out = (U * R2) / (R1 + R2)
    return U_out


def battery_percentage(u_in):
    # Beregn procentdelen af batteriets opladning
    percentage = ((u_in - min_bat_voltage) / (max_bat_voltage - min_bat_voltage)) * 100
    
    # Sørg for, at procentdelen er inden for intervallet 0% til 100%
    percentage = max(0, min(100, percentage))

    return percentage

def read_battery_voltage_avg64():      # Option: average over N times to remove fluctuations
    adc_val = 0
    for i in range(64):
        adc_val += bat_adc.read()      
    voltage = bat_scaling * (adc_val >> 6) # >> fast divide by 64
    return voltage

while True:

    print(bat_adc.read())
    print(read_battery_voltage_avg64())
    sleep(1)
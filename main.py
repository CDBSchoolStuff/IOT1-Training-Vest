import sys, uselect
from machine import UART, Pin, ADC
from time import sleep, sleep_ms

# Initialiserer ADC objekt på pin 25
battery = ADC(Pin(25, Pin.IN), atten=3)
battery.atten(ADC.ATTN_11DB) # 11db attenuation (150mV - 2450mV)
battery.width(ADC.WIDTH_12BIT) # Bestemmer opløsningen i bits 12 (111111111111 = 4096)


#############################################
# Note to self:
# Noget er helt galt med matematikken. Spænding burde rapporteres som 3.8, men beregningen giver 3.4 (I GIVE UP)


print("Two-way ESP32 remote data system\n")


def calc_spaendingsdeler(U, R1, R2):
    U_out = (U * R2) / (R1 + R2)
    return U_out


max_pin_voltage = 3.3
max_bat_voltage = 4.2
min_bat_voltage = 3.0

modstand1 = 4.7
modstand2 = 9.92

spaendingsdeler_max = calc_spaendingsdeler(max_bat_voltage, modstand1, modstand2)
# bat_scaling = max_bat_voltage / spaendingsdeler_max

def v_out(v_in):
    return v_in * (modstand1 + modstand2)/modstand2


def battery_percentage(u_in):
    # Beregn procentdelen af batteriets opladning
    percentage = ((u_in - min_bat_voltage) / (max_bat_voltage - min_bat_voltage)) * 100
    
    # Sørg for, at procentdelen er inden for intervallet 0% til 100%
    percentage = max(0, min(100, percentage))

    return percentage

def calc_skalering(R1, R2):
    #return R2 / (R1 + R2)
    return (R1 + R2) / R2


spaending_scale = calc_skalering(modstand1, modstand2)


while True:
    battery_val = battery.read() # Gemmer aflæsningen af ADC objektets read metode i variablen pot_val
    pin_voltage = battery_val * 3.3 / 4095 # Udregner spændingen og gemmer i variabel
    
    bat_voltage = pin_voltage * spaending_scale


    # battery_voltage = adc_voltage * bat_scaling
    
    print("\nAnalog batteri vaerdi:      ", battery_val) # printer 12Bit ADC værdien
    # print("Analog batteri spaending: ", battery_voltage) # Printer spændingen på GPIO 34
    # print("spaendingsdeler_max: ", spaendingsdeler_max)
    print("adc_voltage: ", pin_voltage)
    # print("bat_scaling:", bat_scaling)
    print("Batteriets spaending:", bat_voltage)

    # Udskriv batteriets procentdel
    # print("Batteriets opladningsprocent er:", battery_percentage(bat_voltage), "%")
    
    print("Spaending scale:", spaending_scale)
    
    sleep(1)
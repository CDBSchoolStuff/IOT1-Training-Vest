import sys, uselect
from machine import UART, Pin, ADC
from time import sleep, sleep_ms

# Initialiserer ADC objekt på pin 25
battery = ADC(Pin(25, Pin.IN), atten=3)
battery.atten(ADC.ATTN_11DB) # 11db attenuation (150mV - 2450mV)
battery.width(ADC.WIDTH_12BIT) # Bestemmer opløsningen i bits 12 (111111111111 = 4096)


uart_remote_port = 1
uart_remote_pin_tx = 33
uart_remote_pin_rx = 32
uart_remote_speed = 9600

group_id = 5

uart_remote = UART(uart_remote_port, baudrate = uart_remote_speed, tx = uart_remote_pin_tx, rx = uart_remote_pin_rx)

usb = uselect.poll()
usb.register(sys.stdin, uselect.POLLIN)

#############################################
# Note to self:
# Noget er helt galt med matematikken. Spænding burde rapporteres som 3.8, men beregningen giver 3.4 (I GIVE UP)

#############################################     
#FUNTIONS

#############################################
#PROGRAM


print("Two-way ESP32 remote data system\n")


def calc_spaendingsdeler(U, R1, R2):
    U_out = (U * R2) / (R1 + R2)
    return U_out

max_pin_voltage = 3.3
max_bat_voltage = 4.2

modstand1 = 5.6
modstand2 = 10

spaendingsdeler_max = calc_spaendingsdeler(max_bat_voltage, modstand1, modstand2)
bat_scaling = max_bat_voltage / spaendingsdeler_max

while True:
    battery_val = battery.read() # Gemmer aflæsningen af ADC objektets read metode i variablen pot_val
    
    adc_voltage = battery_val * (3.3 / 4096) # Udregner spændingen og gemmer i variabel
    
    battery_voltage = adc_voltage * bat_scaling
    
    print("Analog batteri vaerdi:      ", battery_val) # printer 12Bit ADC værdien
    print("\nAnalog batteri spaending: ", battery_voltage) # Printer spændingen på GPIO 34
    print("spaendingsdeler_max: ", spaendingsdeler_max)
    print("adc_voltage: ", adc_voltage)
    print("bat_scaling:", bat_scaling)
    sleep(1)




    if uart_remote.any() > 0:
        string = uart_remote.read().decode()
        string = string.strip()
        print("Remote: " + string)

    if usb.poll(0):
        string = sys.stdin.readline()
        sys.stdin.readline()
        string = string.strip()
        print("USB : " + string)

        uart_remote.write(string + "\n")
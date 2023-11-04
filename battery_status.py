from machine import Pin, ADC
from time import sleep, sleep_ms
from neopixel import NeoPixel

class Battery_Status:    
    #########################################################################
    # CONFIGURATION

    # Voltages
    max_bat_voltage = 4.2
    min_bat_voltage = 3.0

    # Battery
    max_adc_val = 2700                                  # Målt Robust = 2700, Fumlebræt 25 = 3400, fumlebræt 32 = 3350
    bat_scaling = max_bat_voltage / max_adc_val         # The battery voltage divider ratio, replace <adc_4v2> with ADC value when 4,2 V applied

    # Resistors
    resistor1 = 4.7
    resistor2 = 10.08                                   # Fumlebræt = 9.92, Robust = 10.08

    
    #########################################################################
    # Class variables
    
    bat_percentage = 0
    avg_bat_percentage = 0
    
    # Opret en tom buffer
    buffer = []
    

    #########################################################################
    # INIT
    
    def __init__(self, bat_adc):
        self.bat_adc = bat_adc


    #########################################################################
    # Functions

    # Ikke brugt
    def calc_spaendingsdeler(self, U, R1, R2):
        U_out = (U * R2) / (R1 + R2)
        return U_out

    def battery_percentage(self, u_in):
        percentage = ((u_in - Battery_Status.min_bat_voltage) / (Battery_Status.max_bat_voltage - Battery_Status.min_bat_voltage)) * 100
        
        percentage = max(0, min(100, percentage))
        return percentage

    def read_battery_voltage_avg64(self):
        adc_val = 0
        for i in range(64):
            adc_val += self.bat_adc.read()      
        voltage = Battery_Status.bat_scaling * (adc_val >> 6)
        return voltage
    
    def calculate_average_battery(self, window_size):
        buffer = self.buffer
        buffer.append(self.bat_percentage)
        if len(buffer) > window_size:
            buffer.pop(0)

        if not buffer:
            return 0
        return sum(buffer) / len(buffer)
    
    def reg_battery_status(self):
        window_size = 20
        
        bat_voltage = self.read_battery_voltage_avg64()
        self.bat_percentage = self.battery_percentage(bat_voltage)
        self.avg_bat_percentage = self.calculate_average_battery(window_size)
    
    def get_bat_percentage(self):
        return self.avg_bat_percentage
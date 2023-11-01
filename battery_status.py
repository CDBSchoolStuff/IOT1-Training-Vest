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
    # pin_adc_bat = 25                       # The battery status input pin
    max_adc_val = 2700                     # Målt Robust = 2700, Fumlebræt 25 = 3400, fumlebræt 32 = 3350
    bat_scaling = max_bat_voltage / max_adc_val        # The battery voltage divider ratio, replace <adc_4v2> with ADC value when 4,2 V applied

    # Resistors
    resistor1 = 4.7
    resistor2 = 10.08                      # Fumlebræt = 9.92, Robust = 10.08

    # NeoPixel
    PIXEL_NUMBER = 12 # number of pixels in the Neopixel ring
    PIXEL_PIN = 26 # pin atached to Neopixel ring

    #########################################################################
    # OBJECTS

    # bat_adc = None
    # bat_adc = ADC(Pin(pin_adc_bat))        # The battery status ADC object
    # bat_adc.atten(ADC.ATTN_11DB)           # Full range: 3,3 V
    # bat_adc.width(ADC.WIDTH_12BIT)         # Bestemmer opløsningen i bits 12 (111111111111 = 4096)

    # Instantierer neopixel som objekt
    # neopixel = NeoPixel(Pin(PIXEL_PIN, Pin.OUT), PIXEL_NUMBER) # create NeoPixel instance

    
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
    # Beregner den teoretiske maksimale spænding for spændingsdeleren.
    def calc_spaendingsdeler(self, U, R1, R2):
        U_out = (U * R2) / (R1 + R2)
        return U_out

    def battery_percentage(self, u_in):
        # Beregn procentdelen af batteriets opladning
        percentage = ((u_in - Battery_Status.min_bat_voltage) / (Battery_Status.max_bat_voltage - Battery_Status.min_bat_voltage)) * 100
        # Sørg for, at procentdelen er inden for intervallet 0% til 100%
        percentage = max(0, min(100, percentage))
        return percentage

    def read_battery_voltage_avg64(self):      # Option: average over N times to remove fluctuations
        adc_val = 0
        for i in range(64):
            adc_val += self.bat_adc.read()      
        voltage = Battery_Status.bat_scaling * (adc_val >> 6) # >> fast divide by 64
        return voltage
    
    def calculate_average_battery(self, window_size):
        buffer = self.buffer
        buffer.append(self.bat_percentage)
        if len(buffer) > window_size:
            buffer.pop(0)  # Fjern ældste værdi, hvis bufferen er fyldt

        if not buffer:
            return 0  # Returner 0, hvis bufferen er tom
        return sum(buffer) / len(buffer)
        
    #########################################################################
    # Program
    
    
    # Denne funktion har til ansvar at opdatere batteri-procent variablen.
    def reg_battery_status(self):
        # Specificer vinduestørrelse (f.eks. 10 eksekveringer)
        window_size = 20
        
        bat_voltage = self.read_battery_voltage_avg64()
        self.bat_percentage = self.battery_percentage(bat_voltage)
        self.avg_bat_percentage = self.calculate_average_battery(window_size)
    
    # Funktion som returnerer batteri procenten
    def get_bat_percentage(self):
        return self.avg_bat_percentage
class Battery_Status:
    from machine import Pin, ADC
    from time import sleep, sleep_ms
    from neopixel import NeoPixel
    
    #########################################################################
    # CONFIGURATION

    # Voltages
    max_bat_voltage = 4.2
    min_bat_voltage = 3.0

    # Battery
    pin_adc_bat = 25                       # The battery status input pin
    max_adc_val = 3400                     # Målt Robust = 2700, Fumlebræt = 3400
    bat_scaling = max_bat_voltage / max_adc_val        # The battery voltage divider ratio, replace <adc_4v2> with ADC value when 4,2 V applied

    # Resistors
    resistor1 = 4.7
    resistor2 = 9.92                      # Fumlebræt = 9.92, Robust = 10.08

    # NeoPixel
    PIXEL_NUMBER = 12 # number of pixels in the Neopixel ring
    PIXEL_PIN = 26 # pin atached to Neopixel ring

    # Button
    pin_adc_button = 4

    #########################################################################
    # OBJECTS

    bat_adc = ADC(Pin(pin_adc_bat))        # The battery status ADC object
    bat_adc.atten(ADC.ATTN_11DB)           # Full range: 3,3 V
    bat_adc.width(ADC.WIDTH_12BIT)         # Bestemmer opløsningen i bits 12 (111111111111 = 4096)

    # Instantierer neopixel som objekt
    neopixel = NeoPixel(Pin(PIXEL_PIN, Pin.OUT), PIXEL_NUMBER) # create NeoPixel instance

    # Instantierer knap som objekt
    pb = Pin(pin_adc_button, Pin.IN)


    #########################################################################
    # INIT
    
    # def __init__(self, bat_adc, pb):
    #      self.bat_adc = bat_adc
    #      self.pb = pb
        
        
        


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
            adc_val += Battery_Status.bat_adc.read()      
        voltage = Battery_Status.bat_scaling * (adc_val >> 6) # >> fast divide by 64
        return voltage

    # Function to map battery percentage to the number of LEDs to light up
    def map_battery_to_leds(battery_percentage):
        # Assuming a linear mapping
        leds_to_light = int(Battery_Status.PIXEL_NUMBER * battery_percentage / 100)
        return leds_to_light

    # Function to update the LED ring based on battery percentage
    def update_led_ring(self, battery_percentage):
        leds_to_light = Battery_Status.map_battery_to_leds(battery_percentage)
        for i in range(Battery_Status.PIXEL_NUMBER):
            if i < leds_to_light:
                Battery_Status.neopixel[i] = (0, 20, 0)  # Green LED
            else:
                Battery_Status.neopixel[i] = (0, 0, 0)  # Off
        Battery_Status.neopixel.write()

    # Funktion som er til ansvar for at nulstille/slukke alle pixels.
    # Funktionen modtager ingen argumenter.
    def clear_led_ring(self):
        for number in range(Battery_Status.PIXEL_NUMBER): # Itererer mellem alle pixels.
            Battery_Status.neopixel[number] = (0, 0, 0) # Sætter den nuværende pixel i iterationen til at have farvekoden "0,0,0" (Dette slukker for dem).
            Battery_Status.neopixel.write()
        
        
    #########################################################################
    # Program
    
    def battery_status(self):
        bat_voltage = self.read_battery_voltage_avg64()
        bat_percentage = self.battery_percentage(bat_voltage)
        # print(bat_adc.read())
        # print(bat_voltage)
        # print(button)

        print("Battery charge percentage:", bat_percentage, "%")

        button = self.pb.value()

        if button == 1:
            self.update_led_ring(bat_percentage)
            print("Updating LED ring")
        else:
            self.clear_led_ring()
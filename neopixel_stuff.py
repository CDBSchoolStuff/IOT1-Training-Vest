from machine import Pin, ADC
from neopixel import NeoPixel

class NeoPixel_Stuff:
    #########################################################################
    # CONFIGURATION

    PIXEL_NUMBER = 12 # number of pixels in the Neopixel ring
    PIXEL_PIN = 26 # pin atached to Neopixel ring
    
    # Button
    pin_adc_button = 4
    
    #########################################################################
    # OBJECTS
    # Instantierer neopixel som objekt
    neopixel = NeoPixel(Pin(PIXEL_PIN, Pin.OUT), PIXEL_NUMBER) # create NeoPixel instance
    
    # Instantierer knap som objekt
    pb = Pin(pin_adc_button, Pin.IN)
    
    
    #########################################################################
    # INIT
    
    def __init__(self, Battery, Tackling):
        self.Battery = Battery
        self.Tackling = Tackling
    
    
    #########################################################################
    # Functions
    
    # Funktion som er til ansvar for at nulstille/slukke alle pixels.
    # Funktionen modtager ingen argumenter.
    def clear_led_ring(self):
        for number in range(self.PIXEL_NUMBER): # Itererer mellem alle pixels.
            self.neopixel[number] = (0, 0, 0) # Sætter den nuværende pixel i iterationen til at have farvekoden "0,0,0" (Dette slukker for dem).
            self.neopixel.write()

    # Funktion som er ansvarlig for at sætte alle pixels farve på en gang.
    # Funktionen modtager 3 argumenter; red, green, blue. Disse henviser til en RGB farvekode.
    def set_color_all(self, red, green, blue):
        for number in range(self.PIXEL_NUMBER): # Itererer mellem alle pixels.
            self.neopixel[number] = (red, green, blue) # Sætter den nuværende pixel i iterationen til den angivede farve.
        self.neopixel.write() # Skriver værdi til pixel.
            
        # Function to map battery percentage to the number of LEDs to light up
    def map_battery_to_leds(self, battery_percentage):
        # Assuming a linear mapping
        leds_to_light = int(self.PIXEL_NUMBER * battery_percentage / 100)
        return leds_to_light

    # Function to update the LED ring based on battery percentage
    def update_led_ring(self, battery_percentage):
        leds_to_light = self.map_battery_to_leds(battery_percentage)
        for i in range(self.PIXEL_NUMBER):
            if i < leds_to_light:
                self.neopixel[i] = (0, 20, 0)  # Green LED
            else:
                self.neopixel[i] = (0, 0, 0)  # Off
        self.neopixel.write()
        
        
    prev_clear = False
    # Denne funktion har til ansvar at opdatere Neopixel ringen med den nuværende batteri procent.
    def neopixel_battery_status(self):
        #percentage = self.bat_percentage
        percentage = self.Battery.avg_bat_percentage
        button = self.pb.value()
        
        print("Battery charge percentage:", self.Battery.bat_percentage, "%")
        print("Avg battery charge percentage:", self.Battery.avg_bat_percentage, "%")

        if button == 1:            
            self.update_led_ring(percentage)
            print("Updating LED ring")
            self.prev_clear = False
            
        else:
            if self.prev_clear == False:
                self.clear_led_ring()
                self.prev_clear = True
            
    prev_on = False
    val = 0
    def neopixel_tackling(self):
        tackling_amount = self.Tackling.get_tackling_amount()
        
        interval = [10, 20, 30, 40, 50]        
        
        if tackling_amount in interval and self.val < 4:
            if self.prev_on == False:
                self.set_color_all(30,0,0)
                self.prev_on = True
                self.val = self.val + 1
            else:
                self.clear_led_ring()
                self.prev_on = False
        if tackling_amount not in interval:
            self.val = 0
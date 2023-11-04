from machine import Pin, ADC
from neopixel import NeoPixel

class NeoPixel_Stuff:
    #########################################################################
    # CONFIGURATION

    # NeoPixel
    PIXEL_NUMBER = 12
    PIXEL_PIN = 26
    
    # Button
    pin_adc_button = 4
    
    #########################################################################
    # OBJECTS
    neopixel = NeoPixel(Pin(PIXEL_PIN, Pin.OUT), PIXEL_NUMBER) # create NeoPixel instance
    
    pb = Pin(pin_adc_button, Pin.IN)
    
    
    #########################################################################
    # INIT
    
    def __init__(self, Battery, Tackling):
        self.Battery = Battery
        self.Tackling = Tackling
    
    
    #########################################################################
    # Functions
    
    def clear_led_ring(self):
        for number in range(self.PIXEL_NUMBER):
            self.neopixel[number] = (0, 0, 0)
            self.neopixel.write()

    def set_color_all(self, red, green, blue):
        for number in range(self.PIXEL_NUMBER):
            self.neopixel[number] = (red, green, blue)
        self.neopixel.write()
            
    def map_battery_to_leds(self, battery_percentage):
        leds_to_light = int(self.PIXEL_NUMBER * battery_percentage / 100)
        return leds_to_light

    def update_led_ring(self, battery_percentage):
        leds_to_light = self.map_battery_to_leds(battery_percentage)
        for i in range(self.PIXEL_NUMBER):
            if i < leds_to_light:
                self.neopixel[i] = (0, 20, 0)  # Green LED
            else:
                self.neopixel[i] = (0, 0, 0)  # Off
        self.neopixel.write()
        
        
    prev_clear = False

    def neopixel_battery_status(self):
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
            if self.prev_on == True:
                self.clear_led_ring()
                self.prev_on = False
            else:
                self.set_color_all(30,0,0)
                self.prev_on = True
                self.val = self.val + 1
            
        if tackling_amount not in interval:
            self.val = 0
            
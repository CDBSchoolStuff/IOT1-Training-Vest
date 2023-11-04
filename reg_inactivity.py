class Reg_Inactivity:
    #########################################################################
    # CONFIGURATION
    
    inactive_speed = 5.0 # km/t ???
    updates_to_trigger = 5  # Hvor mange gange koden skal køres før at
    
    #########################################################################
    # VARIABLES
    
    trigger_val = 0
    inactivity_amount = 0
    prev_inactive = False
    
    #########################################################################
    # INIT
    
    def __init__(self, GPS, LED_Ring):
         self.GPS = GPS
         self.LED_Ring = LED_Ring
    
    #########################################################################
    # Functions
    
    def reg_inactivity(self):
        speed = self.GPS.speed()
        #print("Speed:", speed)
        
        if speed:
            if speed < self.inactive_speed:
                print("Spilleren er inaktiv!")
                self.trigger_val = self.trigger_val + 1
                if self.prev_inactive == True:
                    self.LED_Ring.set_color_all(30,30,0)
                
            if self.trigger_val >= self.updates_to_trigger and self.prev_inactive == False:
                print("Spilleren har været inaktiv i", self.updates_to_trigger, "opdateringer")                
                self.inactivity_amount = self.inactivity_amount + 1
                print("Spilleren har være inaktiv", self.inactivity_amount, "gange.")
                self.trigger_val = 0
                self.prev_inactive = True
                
            if speed > self.inactive_speed:
                print("Ikke inaktiv, nulstiller!")
                self.LED_Ring.clear_led_ring()
                self.trigger_val = 0
                self.prev_inactive = False
            
    def get_inactivity_amount(self):
        return self.inactivity_amount


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
    
    def __init__(self, GPS):
         self.GPS = GPS
    
    #########################################################################
    # Functions
    
    def reg_inactivity(self):
        speed = self.GPS.speed()
        #print("Speed:", speed)
        
        if speed:
            # Tæller trigger_val op med 1 hver gang at der registreres at spilleren står stille.
            if speed < self.inactive_speed:
                print("Spilleren er inaktiv!")
                self.trigger_val = self.trigger_val + 1
            
            # Tæller inactivity_amount op med 1 og nulstiller trigger_val når trigger_val overgår eller er lig med updates_to_trigger.
            if self.trigger_val >= self.updates_to_trigger and self.prev_inactive == False:
                print("Spilleren har været inaktiv i", self.updates_to_trigger, "opdateringer")                
                self.inactivity_amount = self.inactivity_amount + 1
                print("Spilleren har være inaktiv", self.inactivity_amount, "gange.")
                self.trigger_val = 0
                self.prev_inactive = True
                
            if speed > self.inactive_speed:
                print("Ikke inaktiv, nulstiller!")
                self.trigger_val = 0
                self.prev_inactive = False
            
            return self.inactivity_amount
        else:
            print("Speed not valid. Current inactivity amount:", self.inactivity_amount)
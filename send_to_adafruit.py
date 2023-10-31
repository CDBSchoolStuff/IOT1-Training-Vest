class Send_to_Adafruit:
    
    #########################################################################
    # CONFIGURATION
    
    #########################################################################
    # OBJECTS
    
    #########################################################################
    # INIT
    
    def __init__(self, GPS, mqtt, Tackling, Inactivity):
        self.GPS = GPS
        self.mqtt = mqtt
        self.Tackling = Tackling
        self.Inactivity = Inactivity
        
    
    
    #########################################################################
    # Functions
    
    def gps_to_adafruit(self):
        # Hvis funktionen returnere en string er den True ellers returnere den False
        gps_data = self.GPS.get_adafruit_gps()
        if gps_data: # hvis der er korrekt data så send til adafruit
            print(f'\ngps_data er: {gps_data}')
            self.mqtt.web_print(gps_data, 'chbo0003/feeds/mapfeed/csv') 
        
        
    def tackling_to_adafruit(self):
        tackling_amount = self.Tackling.get_tackling_amount()
        print("Tackling Amount: ", tackling_amount)
        self.mqtt.web_print(tackling_amount, 'chbo0003/feeds/tacklingfeed') 
        
        
    def inactivity_to_adafruit(self):
        inactivity_amount = self.Inactivity.get_inactivity_amount()
        print("Inactivity Amount: ", inactivity_amount)
        self.mqtt.web_print(inactivity_amount, 'chbo0003/feeds/inactivityfeed')
        
        
        
    current_function_index = 0 # Variable to keeps track of the index of the next function to execute
    
    '''
    Denne funktion har til ansvar at eksekvere funktionerne definermqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IOet i functions_to_execute listen. 
    # Hver gang denne funktion kaldes eksikveres den næste funktion i listen, således at vi ikke sender alle data på samme tid og derved undgår vi at blive rate limited af Adafruit IO.
    '''
    def send_to_adafruit(self):
        
        functions_to_execute = [
            self.gps_to_adafruit, 
            self.tackling_to_adafruit, 
            self.inactivity_to_adafruit
        ]
        
        if self.current_function_index < len(functions_to_execute):
            functions_to_execute[self.current_function_index]()
            self.current_function_index += 1
            if self.current_function_index == len(functions_to_execute):
                self.current_function_index = 0  # Reset index to 0 if all functions have been executed
                
        if len(self.mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            self.mqtt.besked = ""
            
        self.mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO
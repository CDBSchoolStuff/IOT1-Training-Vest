class Send_to_Adafruit:
    
    #########################################################################
    # CONFIGURATION
    
    #########################################################################
    # OBJECTS
    
    #########################################################################
    # INIT
    
    def __init__(self, GPS, mqtt):
        self.GPS = GPS
        self.mqtt = mqtt
    
    
    #########################################################################
    # Functions
    
    def gps_to_adafruit(self):
        # Hvis funktionen returnere en string er den True ellers returnere den False
        gps_data = self.GPS.get_adafruit_gps()
        if gps_data: # hvis der er korrekt data så send til adafruit
            print(f'\ngps_data er: {gps_data}')
            self.mqtt.web_print(gps_data, 'chbo0003/feeds/mapfeed/csv') 

        #For at sende beskeder til andre feeds kan det gøres sådan:
        # mqtt.web_print("Besked til anden feed", DIT_ADAFRUIT_USERNAME/feeds/DIT_ANDET_FEED_NAVN/ )
        #Indsæt eget username og feednavn til så det svarer til dit eget username og feed du har oprettet
            
        #For at vise lokationsdata på adafruit dashboard skal det sendes til feed med /csv til sidst
        #For at sende til GPS lokationsdata til et feed kaldet mapfeed kan det gøres således:
        #mqtt.web_print(gps_data, 'DIT_ADAFRUIT_USERNAME/feeds/mapfeed/csv')        
                
        #mqtt.web_print("test1") # Hvis der ikke angives et 2. argument vil default feed være det fra credentials filen      
        #sleep(4)  # vent mere end 3 sekunder mellem hver besked der sendes til adafruit
        if len(self.mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            self.mqtt.besked = ""       
                        
        self.mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        print(".", end = '') # printer et punktum til shell, uden et enter        
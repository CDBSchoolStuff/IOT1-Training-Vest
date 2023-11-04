class Send_to_Adafruit:
    
    #########################################################################
    # INIT
    
    def __init__(self, GPS, mqtt, Tackling, Inactivity, Battery):
        self.GPS = GPS
        self.mqtt = mqtt
        self.Tackling = Tackling
        self.Inactivity = Inactivity
        self.Battery = Battery
        
    
    #########################################################################
    # Functions
    
    def gps_to_adafruit(self):
        gps_data = self.GPS.get_adafruit_gps()
        if gps_data:
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
        
    
    def battery_to_adafruit(self):
        battery_percentage = self.Battery.get_bat_percentage()
        print("Battery Percentage: ", battery_percentage, "%")
        self.mqtt.web_print(battery_percentage, 'chbo0003/feeds/batteryfeed')
        
        
    current_function_index = 0 

    def send_to_adafruit(self):
        
        functions_to_execute = [
            self.gps_to_adafruit, 
            self.tackling_to_adafruit, 
            self.inactivity_to_adafruit,
            self.battery_to_adafruit
        ]
        
        if self.current_function_index < len(functions_to_execute):
            functions_to_execute[self.current_function_index]()
            self.current_function_index += 1
            if self.current_function_index == len(functions_to_execute):
                self.current_function_index = 0
                
        if len(self.mqtt.besked) != 0:
            self.mqtt.besked = ""
            
        self.mqtt.sync_with_adafruitIO()
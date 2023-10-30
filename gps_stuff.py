class GPS_Stuff:
    from gps_bare_minimum import GPS_Minimum
    from machine import UART
    
    #########################################################################
    # CONFIGURATION
    gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
    gps_speed = 9600                           # UART speed, defauls u-blox speed

    #########################################################################
    # OBJECTS
    uart = UART(gps_port, gps_speed)           # UART object creation
    gps = GPS_Minimum(uart)                    # GPS object creation


    #########################################################################
    # Functions

    def get_adafruit_gps(self):
        speed = lat = lon = None # Opretter variabler med None som værdi
        if self.gps.receive_nmea_data():
            # hvis der er kommet end bruggbar værdi på alle der skal anvendes
            if self.gps.get_speed() != -999 and self.gps.get_latitude() != -999.0 and self.gps.get_longitude() != -999.0 and self.gps.get_validity() == "A":
                # gemmer returværdier fra metodekald i variabler
                speed = str(self.gps.get_speed())
                lat = str(self.gps.get_latitude())
                lon = str(self.gps.get_longitude())
                # returnerer data med adafruit gps format
                return speed + "," + lat + "," + lon + "," + "0.0"
            else: # hvis ikke både hastighed, latitude og longtitude er korrekte 
                print(f"GPS data to adafruit not valid:\nspeed: {speed}\nlatitude: {lat}\nlongtitude: {lon}")
                return False
        else:
            return False

    def speed(self):
        return self.gps.get_speed()


    #########################################################################
    # PROGRAM
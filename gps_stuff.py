class GPS_Stuff:
    from gps_bare_minimum import GPS_Minimum
    from machine import UART
    
    #########################################################################
    # CONFIGURATION
    gps_port = 2
    gps_speed = 9600

    #########################################################################
    # OBJECTS
    uart = UART(gps_port, gps_speed)
    gps = GPS_Minimum(uart)


    #########################################################################
    # Functions

    def get_adafruit_gps(self):
        speed = lat = lon = None
        if self.gps.receive_nmea_data():
            if self.gps.get_speed() != -999 and self.gps.get_latitude() != -999.0 and self.gps.get_longitude() != -999.0 and self.gps.get_validity() == "A":
                speed = str(self.gps.get_speed())
                lat = str(self.gps.get_latitude())
                lon = str(self.gps.get_longitude())
                return speed + "," + lat + "," + lon + "," + "0.0"
            else:
                print(f"GPS data to adafruit not valid:\nspeed: {speed}\nlatitude: {lat}\nlongtitude: {lon}")
                return False
        else:
            return False

    def speed(self):
        speed = None
        if self.gps.receive_nmea_data():
            if self.gps.get_speed() != -999:
                speed = float(self.gps.get_speed())
                return speed
            else:
                return False
        else:
            return False
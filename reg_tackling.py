from time import sleep
from machine import I2C, Pin
from mpu6050 import MPU6050
import sys

#########################################################################
# CONFIGURATION



# Diverse variabler:
standing_threshold = 10000 # Ansvarlig for stejlheden af hvornår enheden betegnes som værende stående eller liggende.
number_of_falls = 0
prev_standing = False

#########################################################################
# OBJECTS

#Initialisering af I2C objekt
i2c = I2C(0)

#Initialisering af mpu6050 objekt
imu = MPU6050(i2c)


#########################################################################
# Functions



#########################################################################
# PROGRAM

def reg_tackling_thread():
    while True:
        try:
            # printer hele dictionary som returneres fra get_values metoden
            imu_data = imu.get_values()
            print(imu_data)

            if (imu_data.get("acceleration x") > standing_threshold or imu_data.get("acceleration x") < -standing_threshold) or (imu_data.get("acceleration y") > standing_threshold or imu_data.get("acceleration y") < -standing_threshold):
                print("Enheden står op!")
                prev_standing = True
            else:
                    print("Spilleren er blevet tacklet!")
                    
                    # --------- Del 3 ---------
                    if prev_standing == True: # Sørger for at antallet af fald kun inkrementeres hvis der gåes fra stående til liggende tilstand.
                        number_of_falls = number_of_falls + 1
                        print("Antal fald:", number_of_falls)
                        # --------- Del 6 ---------
                        # mqtt.web_print(number_of_falls, 'chbo0003/feeds/ESP32feed')
                        # -------------------------
                    # -------------------------
            sleep(1)
        except KeyboardInterrupt:
            print("Ctrl+C pressed - exiting program.")
            sys.exit()
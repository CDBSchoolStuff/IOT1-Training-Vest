from time import sleep
from machine import I2C, Pin
from mpu6050 import MPU6050
import sys

class Reg_Tackling:
    #########################################################################
    # CONFIGURATION

    standing_threshold = 10000


    #########################################################################
    # CLASS VARIABLES

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

    def reg_tackling(self):
        try:
            imu_data = self.imu.get_values()

            if (imu_data.get("acceleration x") > self.standing_threshold or imu_data.get("acceleration x") < -self.standing_threshold) or (imu_data.get("acceleration y") > self.standing_threshold or imu_data.get("acceleration y") < -self.standing_threshold):
                self.prev_standing = True
            else:
                    if self.prev_standing == True:
                        self.number_of_falls = self.number_of_falls + 1
                        print("Antal fald:", self.number_of_falls)
                        self.prev_standing = False
        except:
            print("reg_tackling error, exception caught!")
                  
    
    def get_tackling_amount(self):
        return self.number_of_falls
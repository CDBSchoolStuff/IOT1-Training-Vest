from battery_status import battery_status_thread
from gps_to_adafruit import gps_to_adafruit_thread

import _thread

#########################################################################
# Execute threads

_thread.start_new_thread(battery_status_thread, ())
#_thread.start_new_thread(gps_to_adafruit_thread, ())
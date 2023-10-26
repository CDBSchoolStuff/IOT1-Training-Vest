import battery_status
import gps_status
import _thread


#########################################################################
# Execute threads

_thread.start_new_thread(battery_status.thread, ())
_thread.start_new_thread(gps_status, ())
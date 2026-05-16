import Parameters as p
import time as t
def SafeLand():
    p.vehicle.mode = "RTL"
    p.vehicle.flush()
    while p.vehicle.armed:
        print(" Global Location (relative altitude): %s" %p.vehicle.location.global_relative_frame)
        t.sleep(1)
    print("Motors Disarmed at %s" %p.vehicle.location.global_relative_frame)
    print("Closing Script")

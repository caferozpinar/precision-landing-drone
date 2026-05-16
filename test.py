"""
Simple script for take off and control with arrow keys
"""


import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import math
import keyboard  # using module keyboard



#-- Connect to the vehicle
print('Connecting...')
vehicle = connect('tcp:127.0.0.1:5762')



 #-- Define the function for sending mavlink velocity command in body frame
def set_velocity_body(vehicle, vx, vy, vz):
    """ Remember: vz is positive downward!!!
    http://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html
    
    Bitmask to indicate which dimensions should be ignored by the vehicle 
    (a value of 0b0000000000000000 or 0b0000001000000000 indicates that 
    none of the setpoint dimensions should be ignored). Mapping: 
    bit 1: x,  bit 2: y,  bit 3: z, 
    bit 4: vx, bit 5: vy, bit 6: vz, 
    bit 7: ax, bit 8: ay, bit 9:
    
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, #-- BITMASK -> Consider only the velocities
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()


hiz = 50

set_velocity_body(vehicle, hiz, 0, 0)
time.sleep(20)
set_velocity_body(vehicle, 0, 0, 0)

while False:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        kp = 0
        if keyboard.is_pressed('w'):  # if key 'q' is pressed 
            set_velocity_body(vehicle, hiz, 0, 0)
            kp = 1
        if keyboard.is_pressed('d'):  # if key 'q' is pressed 
            set_velocity_body(vehicle, 0, hiz, 0)
            kp = 1
        if kp == 0:
            set_velocity_body(vehicle, 0, 0, 0)

    except:
        break  # if user pressed a key other than the given key the loop will break
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
      
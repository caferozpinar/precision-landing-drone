"""
Simple script for take off and control with arrow keys
"""


import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal

#-- Connect to the vehicle
print('Connecting...')
vehicle = connect('/dev/ttyAMA0')
print('Connectted')

vehicle.gimbal.rotate(0, 0, 0)    
time.sleep(0.5)

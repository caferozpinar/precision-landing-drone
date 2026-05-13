import sensor
import image
import time
import math
import pyb
from pyp import UART
from ulab import numpy as np

#check is script successfully started.
led = pvp.LED(3)
led.on()
time.sleep(5)#sleep 5 seconds
led.off()
class vectors:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    
    def distance_two_points(point1,point2):
        distance_two_points_unit = math.sqrt((point2.x - point1.x)**2 + (point1.y,point2.y))
        return distance_two_points_unit
    
    def shape_rotation(min,max):
        cos_x = min.x - max.x
        sin_y = min.y - max.y
        shape_angle_rad = math.atan2(cos_x, sin_y)
        shape_angle_deg = math.degrees(shape_angle_rad)
        return shape_angle_deg
    
class raspberry:
    def __init__(self):
        pass
        
class cam:
    def __init__(self,heightfov,widthfov,heigth_px,width_px,cam_lens_size):
        sensor.reset()
        sensor.set_pixformat(sensor.GRAYSCALE)
        sensor.set_framesize(sensor.QVGA)
        clock = time.clock()
        self.heightfov = 0
        self.widthfov = 0
        self.height_px = 0
        self.width_px = 0
        self.cam_lens_size = 1.8

    def led(state):
        if state:
            led.on()
        else:
            led.off()


#check if main script is running
if __name__ == "__main__":
    camera = cam(heightfov = 70.8,widthfov = 55.6,
    heigth_px = 320,width_px = 240,cam_lens_size = 1.8)



    pass



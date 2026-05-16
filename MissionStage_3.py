import Parameters as p
import time
import Camera
import Detect
from MotionControl import TrackCoordinates, DecreaseAltitude, CheckDisarmAltitude, DisarmMotors
import sys
whitePointCenters = None
checkTimer = True
def __FindAverage(array):
    for a in array:
        p1x += a[0][0]
        p1y += a[0][1]
        p2x += a[1][0]
        p2y += a[1][1]
        p3x += a[2][0]
        p3y += a[2][1]
        p4x += a[3][0]
        p4y += a[3][1]
    p1x /= len(array)
    p1y /= len(array)
    p2x /= len(array)
    p2y /= len(array)
    p3x /= len(array)
    p3y /= len(array)
    p4x /= len(array)
    p4y /= len(array)
    return [[p1x, p1y], [p2x, p2y], [p3x, p3y], [p4x, p4y]]



def MissionStage_3():
    print("MissionStage_3 start")
    timeoutTimer = time.time()
    while True:
        
        frame = Camera.GetNextFrame(p.vehicleCameraType)
        whitePointCenters = Detect.Color("POINTS", frame)
        markerCenters = Detect.Marker(whitePointCenters, "BASIC")
        if len(markerCenters) > 1:
            markerCenters = __FindAverage(markerCenters)
        elif len(markerCenters) > 0:
            markerCenters = markerCenters[0]
        if len(markerCenters) > 0:
            timeoutTimer = time.time()
            TrackCoordinates(markerCenters, p.centerPoint)
            DecreaseAltitude(markerCenters, p.centerPoint)
            
            disarm = CheckDisarmAltitude()
            if disarm:
                DisarmMotors()
                print("MissionStage_3 end")
                sys.exit()
                break
        
        else:
            disarm = CheckDisarmAltitude()
            if disarm:
                DisarmMotors()
                print("MissionStage_3 end")
                Camera.CloseCam(p.vehicleInternalCameraSource)
                sys.exit()
                break
            if time.time() - timeoutTimer > p.detectionTimeout:
                print("Shape Detection Timeout.")
                raise TimeoutError
                    

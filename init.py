import Parameters as p
import dronekit
from cv2 import VideoCapture
__vehicle = None

def __CheckArdupilotConnection():
    try:
        if p.vehicleType == 0:
            __vehicle = dronekit.connect(p.vehicleConnectionIP, wait_ready = p.vehicleConnectionWaitReady, baud = p.vehicleConnectionBaudrate, rate = p.vehicleConnectionRate, timeout = p.vehicleConnectionTimeout)
        else:
             __vehicle = dronekit.connect(p.vehicleConnectionIP)
        print(" Is Armable?: %s" % __vehicle.is_armable)
        print(" System status: %s" % __vehicle.system_status.state)
        p.vehicle = __vehicle
    except Exception as e:
        print("Ardupilot Communication Error")
        print(e)
        raise e

def __checkLidarStatus():
    if p.vehicleEnableLidar:
        try:
            if p.vehicle.rangefinder.distance != None or p.vehicle.rangefinder.voltage != None:
                print(" Rangefinder distance: %s" % p.vehicle.rangefinder.distance)
                print(" Rangefinder voltage: %s" % p.vehicle.rangefinder.voltage)
            else:
                print("Rangefinder connection failed.")
                raise ConnectionError
        except Exception as e:
            print(e)
            raise e
    pass
def __checkGimballStatus():
    if p.vehicleEnableGimball:
        if p.vehicle.gimbal.pitch != None or p.vehicle.gimbal.roll != None or p.vehicle.gimbal.yaw != None:
            print(" Gimbal status: %s" % p.vehicle.gimbal.pitch)
        else:
            print("Gimball Connection Failed.")
            raise ConnectionError
    pass

def __checkCameraStatus():
    if p.vehicleCameraType == 0:
        try:
            capture = VideoCapture(p.vehicleInternalCameraSource)
            ret, frame = capture.read()
            if ret:
                print("camera capture: %s" %capture)
            else:
                raise ConnectionError
            p.capture = capture
        except Exception as e:
            print(e)
            raise e
    pass

def __checkGroundVehicleStatus():
    pass

def __checkWirelessConnection():
    pass

def __checkTelemetryConnection():
    pass

def init():
    """
    initalize the drone system with given parameters from Parameters.py.
    if any error occures during initalizing, raises Error.
    Highly recommended to use with try except block.
    """
    # check ardupilot connection
    __CheckArdupilotConnection()
    # check Lidar Status
    __checkLidarStatus()
    # check gimball status
    __checkGimballStatus()
    # check camera status
    __checkCameraStatus()
    # check ground vehicle status
    __checkGroundVehicleStatus()
    # check wireless connection
    __checkWirelessConnection()
    # check telemetry connection
    __checkTelemetryConnection()

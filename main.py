
#import dronekit
import cam
import shapeFinder
import motion_control
import cProfile
#2592 1944

camera_threshold = (0, 0, 169), (179, 34, 255)
finder_threshold = 10.0, 3.0, 1.5
pointer_location = 1 #set mode 

distance_pos_ref = 0
Kp_pos = 0
Kp_vel = 0
Ki_vel = 0
Ui_vel_integ = 0
Upi_max = 3

distance_height_ref = 30
Kp_height = 0
Kp_height_vel = 0
Ki_height_vel = 0
Ui_height_vel = 0
Upi_heigth_max = 0


class precisionLand():

    def __init__(self):
        pass
    
    def initalize(self):
        try:
            self.camera = cam.colorDetect()
            self.camera.captureCam(1)
            self.camera.setThreshold(camera_threshold)
            self.TFinder = shapeFinder.TFinder()
            self.TFinder.setThreshold(finder_threshold)
            self.vehicle = motion_control.uav("dev/ttyAMA0", baudrate=921600, heartbeat_timeout=180)
            self.vehicle.printStatus()
            self.vehicle.setMultiplier(distance_pos_ref, Kp_pos, Kp_vel, Ki_vel, Ui_vel_integ, Upi_max)

            return 0
        except:
            return 1
    def takeoffAndQuest(self, takeoff_alt):
        success = motion_control.uav.prearmCheck(self.vehicle)
        if success == 1:
            return 1
        motion_control.uav.armThrottle(self.vehicle)
        motion_control.uav.takeoff(self.vehicle, takeoff_alt)
        return 0

    def goPointerCoordinates(self, landing_mode):
        try:
            print("checking landing mode")
            if landing_mode == 1:
                self.vehicle.simple_goto(pointer_location, groundspeed=10)
            else:
                #connect rover telemetry and go readed coordinates
                # this attr disabled now
                pass
            return 0
        except:
            return 1
    def Find(self):
        centers = self.camera.detect()
        success, self.Tshape = self.TFinder.findShape(centers)
        if success == 0:return 0
        if success == 1:return 1
        if success == 2:return 2
    def headPointer(self):
        self.vehicle.trackCoordinates(self.Tshape, self.camera.resolution)

    def RTL():
        pass

if __name__ == "__main__":
    #do only once per script
    while True:
        precise = precisionLand()
        init = precise.initalize()
        if init:
            print("initalize failed")
            print("Exit with Error code : 1")
            break
        quest = precise.takeoffAndQuest(10)
        if quest:
            print("Prearm checks failed")
            print("Exit with error code 2")
            break
        break
    # do while done
    pointer_missing = 1
    shape_not_detected = 0
    need_pid = 0
    while True:
        # 1 : predefined coordinates, 2 : connect rover and track
        if pointer_missing:
            point = precise.goPointerCoordinates(1)
            if point:
                print("Targeting pointer failed")
                precise.RTL()
                print("Exit with error code 3")
                break
            pointer_missing = 0
            shape_not_detected = 1
        if shape_not_detected:
            shape = precise.Find()
            if shape == 1:
                print("Camera Error")
                precise.RTL()
                print("Exit with Error code 4")
                break
            elif shape == 2:
                pointer_missing = 1
                need_pid = 0
            else:
                need_pid = 1
                pointer_missing = 0
        if need_pid:
            pid = precise.headPointer()
            if pid == 0:
                print("landed successfully")
                print("exiting script with success")
                break
            if pid == 1:
                print("Unkown Error")
                print("Exit with Error code 5")
                break
            if pid == 2:
                need_pid = 0
                pointer_missing = 1         
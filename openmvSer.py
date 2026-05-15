import time
import serial

class mvserial():

    def __init__(self, fps):
        self.leave_thread = 0
        self.fps = fps
        self.inner_centers = []
        self.elma = serial.Serial("COM7")
        print(self.elma.name)

    def talkOpen(self):
        time.sleep(self.fps)
        value  = self.elma.read()
        self.inner_centers = value
    
    def pullvalue(self):
        return self.inner_centers
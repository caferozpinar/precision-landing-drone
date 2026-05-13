import cv2 as cv2
import numpy

class detector:
    def __init__(self,lower = (0,0,0),upper = (0,0,0)):
        self.detected_centers = numpy.array([[0]*4]*15)
        self.lower = lower
        self.upper = upper

    def detect_centers(self,source = None ,test = False):
        
        cap = cv2.VideoCapture(source)

        success ,captured_image = cap.read()

        if not success:
            return -1 ,0

        hsv_image = cv2.cvtColor(captured_image,cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_image,self.lower,self.upper)

        contours ,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


        
        val = 0
        if len(contours) != 0:
            for contours in contours:
                x,y,width,height = cv2.boundingRect(contours)
                self.detected_centers[val][0] = (x)
                self.detected_centers[val][1] = (y)
                self.detected_centers[val][2] = (width)
                self.detected_centers[val][3] = (height)
                val += 1
                cv2.rectangle(captured_image, (x,y), (x+width,y+height), (255,0,0), 2, 1)

        cv2.imshow("mask",captured_image)


        return success ,self.detected_centers

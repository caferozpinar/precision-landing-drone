import cv2

class blobDetect():

    def __init__(self):
        pass

    def captureCam(self):
        pass

    def setThreshold(self):
        pass

    def detect(self):
        pass

class colorDetect():

    def __init__(self):
        self.lower_threshold = (0, 0, 0)
        self.upper_threshold = (0, 0, 0)
        print("Detector initilaziton --DONE--")
    
    def showFrame(self, shapes):

        success, frame = self.capture.read()
        for centers in shapes:
            for center in centers:
                x = int(center[0])
                y = int(center[1])
                cv2.circle(frame, (x, y), 3, (0, 0, 255), 3)

        cv2.imshow("test frame", frame)

        k = cv2.waitKey(1) & 0xff
        if k == 27 :
            self.capture.release()
            cv2.destroyAllWindows()
            return 0
        
        return 1

    # Capture camera source
    def captureCam(self, source):
        self.capture = cv2.VideoCapture(source)
        success, frame = self.capture.read()
        self.resolution = frame.shape

        if not success:
            print("ERROR WHILE READING CAMERA SOURCE")
            return -1

        print("Camera capture --DONE-- \nCapture adress: " + str(self.capture),end="\n")

        return 1

    def camRelease(self):
        self.capture.release()
        print("Camera release --DONE--",end="\n")
    
    # Set detection threshold
    def setThreshold(self, lower_threshold, upper_threshold):
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        print("Detector threshold set --DONE-- \nLower threshold values : "+ str(lower_threshold) +" \nUpper threshold values : "+ str(upper_threshold),end="\n")


    def detect(self):
        detected_centers = []
        success, frame = self.capture.read()

        if not success:
            return -1, detected_centers
        
        # Convert captured frame bgr to hsv format
        hsvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Mask converted image in given range
        maskedimage = cv2.inRange(hsvimage, self.lower_threshold, self.upper_threshold)

        # Find contours on masked image
        noidea, contours, hieracry = cv2.findContours(maskedimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Calculate detected centers
        for contours in contours:
            x, y, width, height = cv2.boundingRect(contours)
            x += width/2
            y += height/2
            detected_centers.insert(0,(x,y))
            x = 0
            y = 0
        if len(detected_centers) == 0 : return 2, detected_centers
        else : return 1, detected_centers
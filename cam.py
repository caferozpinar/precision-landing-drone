import cv2

class colorDetect():

    #initalize detector object
    def __init__(self):
        self.lower_threshold = (0, 0, 0)
        self.upper_threshold = (0, 0, 0)
        print("Detector initilaziton --DONE--")

    #capture camera and set resolution for once
    def captureCam(self, source):
        self.capture = cv2.VideoCapture(source)
        success, frame = self.capture.read()
        self.resolution = frame.shape

        if not success:
            print("Error while reading camera source")
            return -1
        
        print("Camera capture --DONE-- \nCapture adress: " + str(self.capture),end="\n")
        return 1
    
    # Set detection threshold
    def setThreshold(self, lower_threshold, upper_threshold):
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        print("Detector threshold set --DONE-- \nLower threshold values : "+ str(lower_threshold) +" \nUpper threshold values : "+ str(upper_threshold),end="\n")

    def detect(self):
        detected_centers = []
        success, frame = self.capture.read()

        if not success:
            return 1, detected_centers
        
        # Convert captured frame bgr to hsv format
        hsvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Mask converted image in given range
        maskedimage = cv2.inRange(hsvimage, self.lower_threshold, self.upper_threshold)

        # Find contours on masked image
        no_idea, contours, hieracry = cv2.findContours(maskedimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Calculate detected centers
        for contours in contours:
            x, y, width, height = cv2.boundingRect(contours)
            x += width/2
            y += height/2
            detected_centers.insert(0,(x,y))
            x = 0
            y = 0
        if len(detected_centers) == 0 : return 2, detected_centers
        else : return 0, detected_centers
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
    
    # Capture camera source
    def captureCam(self, source):
        self.capture = cv2.VideoCapture(source)
        success, frame = self.capture.read()

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
            return detected_centers
        
        # Convert captured frame bgr to hsv format
        hsvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Mask converted image in given range
        maskedimage = cv2.inRange(hsvimage, self.lower_threshold, self.upper_threshold)

        # Find contours on masked image
        contours, hierarchy = cv2.findContours(maskedimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # If none of the contours are detected, return the empty container
        if not len(contours):
            return detected_centers
        
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
    
    def initTracker(self, tracker_type = "KCF"):
        tracker_type = tracker_type.upper()

        if tracker_type == 'BOOSTING':
            self.tracker = cv2.legacy.TrackerBoosting_create()
        if tracker_type == 'MIL':
            self.tracker = cv2.TrackerMIL_create() 
        if tracker_type == 'KCF':
            self.tracker = cv2.TrackerKCF_create() 
        if tracker_type == 'TLD':
            self.tracker = cv2.legacy.TrackerTLD_create() 
        if tracker_type == 'MEDIANFLOW':
            self.tracker = cv2.legacy.TrackerMedianFlow_create() 
        if tracker_type == 'MOSSE':
            self.tracker = cv2.legacy.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            self.tracker = cv2.TrackerCSRT_create()
    

    def roiTracker(self, roi, test = "False"):
        success, frame = self.capture.read()
        
        if not success:
            print("Cannot read frame")
            self.camRelease()
            return 2
        track_notsuccess = self.tracker.init(frame, roi)
        
        if track_notsuccess:
            self.camRelease()
            print("Tracker initalization failed")
            return 3

        print("Tracker succesfully initalized")

        while True:
            success, frame = self.capture.read()
            
            if not success:
                print("Cannot read frame")
                self.camRelease()
                cv2.destroyAllWindows()
                return 2
            
            track_success, roi = self.tracker.update(frame)

            center = roi[0] + (roi[2] / 2) , roi[1] + (roi[3] / 2)
            print(center)
            if track_success and test:
                p1 = (int(roi[0]), int(roi[1]))
                p2 = (int(roi[0] + roi[2]), int(roi[1] + roi[3]))
                cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            
                
            
            else:
                print("Tracking failed")
                return 4
            
            cv2.imshow("test", frame)
            k = cv2.waitKey(1) & 0xff
            if k == 27 :
                self.capture.release()
                cv2.destroyAllWindows()
                return 0


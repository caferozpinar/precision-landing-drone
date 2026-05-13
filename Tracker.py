import cv2
from Follow_Point import Folow_Point

class ROI_tracker:
    def __init__(self, source, tracker_type="KCF",horitzonal_PID = (0,0,0),vertical_PID = (0,0,0)):
        self.source = source
        self.vertical_PID = vertical_PID
        self.horitzonal_PID = horitzonal_PID
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

    def ROI(self,ROI):
        #create point follower
        point = Folow_Point(self.horitzonal_PID,self.vertical_PID)
        #capture video frame
        video = cv2.VideoCapture(self.source)
        #read captured frame
        ret , frame = video.read()
        
        #if readin frame fail print error and exit
        if not ret:
            print('cannot read the video')
            video.release()
            return 0
        
        #initalize tracker object 
        ret = self.tracker.init(frame,ROI)

        #tracking loop
        while True:
            #read video frame
            ret, frame = video.read()

            #if reading frame fails print error and exit
            if not ret:
                print('something went wrong')
                video.release()
                cv2.destroyAllWindows()
                return 0
            #update tracker and get new region of interest
            ret, ROI = self.tracker.update(frame)

            #draw rectangle in screen
            if ret:
                p1 = (int(ROI[0]), int(ROI[1]))
                p2 = (int(ROI[0] + ROI[2]), int(ROI[1] + ROI[3]))
                cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
                #point.follow(ROI)
                

            #if tracking fail return "-1" and detect again
            else:
                print("track failed")
                return -1
            
            cv2.imshow("Tracking", frame)
            k = cv2.waitKey(1) & 0xff
            if k == 27 :
                video.release()
                cv2.destroyAllWindows()
                return 0     
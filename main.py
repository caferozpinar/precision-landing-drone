
#importing libraries
from Detect import detector
from Tracker import ROI_tracker
from Calculate import calculator

#variable definition
source = "track_test.mp4"
landing = False

if __name__ == "__main__":
    #create detector object [(lower threshold), (upper threshold)]
    white_detector = detector((0,0,169),(179,34,255))
    #create calculator object
    calculate = calculator()
    #create tracker object [(video source) , (tracker_type) ,(horitzonal P,I,D), (vertical P,I,D)]
    track = ROI_tracker(source,"KCF",(1,1,1),(1,1,1))

    while True:
        
        #try detecting object if not detect exit and land
        try:
            ret ,centers = white_detector.detect_centers(source)
        except NameError:
            print("Something went wrong when detecting object")
            landing = True
            break
        
        #try to find region of interest
        try:
            if ret :
                Regionofinterest = calculate.ROI(centers)
            else:
                landing = True
                break
        except NameError:
            print("Something went wrong when calculating ROI")

        #track and process object in while loop
        while ret :
            track_ret = track.ROI(Regionofinterest)

            if track_ret == -1:
                break
            else :
                landing = True
                break
            

        if landing:
            break
    
    print("landing")
    print("exiting script ...")
    print("script exited with code %d"%ret)
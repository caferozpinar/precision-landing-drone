import cv2
import time

frame = cv2.VideoCapture(0)


# import the opencv library
import cv2
  
sensitivity = 90
# define a video capture object
vid = cv2.VideoCapture(0)
  
while(True):
    t = time.time()
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    masked = cv2.inRange(frame, (0, 120, 0), (179, 255, 255))
    print(time.time()- t)
    # Display the resulting frame
    cv2.imshow('frame', masked)
    cv2.imshow('frame2', frame)
    cv2.imshow('frame3', hsv)
    
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
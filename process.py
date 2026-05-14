import cv2 as cv2
import numpy
import find
upper = (179,34,255)
lower = (0,0,169)
detected_centers = []
centers = []
linears = []
equals = []
branch = []

linear_thresh = 10.0
gap_thresh = 4.0
branch_thresh = 3.0

def detect_centers(source = None ,test = False):

    #cap = cv2.VideoCapture(1)
    #success ,captured_image = cap.read()
    success = True
    captured_image = cv2.imread("test4.jpg")
    if not success:
        return -1 ,0

    hsv_image = cv2.cvtColor(captured_image,cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_image,lower,upper)

    contours ,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    if len(contours) != 0:
        for contours in contours:
            x,y,width,height = cv2.boundingRect(contours)
            x = (x + (width/2))
            y = (y + (height/2))
            detected_centers.insert(0,(x,y))
            x = 0
            y = 0
            cv2.rectangle(captured_image, (x,y), (x+width,y+height), (255,0,0), 2, 1)

    

    return detected_centers

def draw(array):
    captured_image = cv2.imread("test4.jpg")
    for i in array:
        for z in i:
            cv2.circle(captured_image,(int(z[0]),int(z[1])),5,(0,0,255),4)
        
    cv2.imshow("test",captured_image)
    


if __name__ == "__main__":
    
    finder = find.find_T(linear_thresh,gap_thresh,branch_thresh)
    centers = detect_centers()
    if centers: linears = finder.checkLinear(centers)
    if linears: equals = finder.checkEqualGap(linears)
    if equals: branch = finder.check_branch(equals,centers)
    draw(branch)
    cv2.waitKey(0)
    
    


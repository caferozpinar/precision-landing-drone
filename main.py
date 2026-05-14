import cv2
import numpy
import find
import time
upper = (179,34,255)
lower = (0,0,169)
detected_centers = []
centers = []
linears = []
equals = []
branch = []

linear_thresh = 10.0
gap_thresh = 3.0
branch_thresh = 2.0

black = cv2.imread("blackscreen.jpg")
cap = cv2.VideoCapture("C:/Users/ozpin/Documents/My_Workspace/TEKNOFEST-2023/SERBEST-GÖREV/Precision_land_software/DRONE SOFTWARE/Media/track_test.mp4")


def detect_centers(source = None ,test = False):
    success ,captured_image = cap.read()
    # success = True
    # captured_image = cv2.imread("test4.jpg")
    if not success:
        return -1

    hsv_image = cv2.cvtColor(captured_image,cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_image,lower,upper)

    contours ,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    if len(contours) != 0:
        detected_centers.clear()
        for contours in contours:
            x,y,width,height = cv2.boundingRect(contours)
            x = (x + (width/2))
            y = (y + (height/2))
            detected_centers.insert(0,(x,y))
            x = 0
            y = 0
            #cv2.rectangle(captured_image, (x,y), (x+width,y+height), (255,0,0), 2, 1)
    
    return detected_centers

def draw(array):
    success ,captured_image = cap.read()
    test = captured_image
    # cv2.rectangle(black,(0,0),(1913,1046),(0,0,0),-1)
    cv2.imshow("gercek frame", test)
    for z in array:
        # for z in i:
            cv2.circle(captured_image,(int(z[0]),int(z[1])),7,(0,0,255),4)
    
    
    cv2.imshow("test frame",captured_image)
    cv2.waitKey(0)
    test = black
    cv2.destroyAllWindows()

if __name__ == "__main__":

    finder = find.find_T(linear_thresh,gap_thresh,branch_thresh)
    while(1):

        centers = detect_centers()
        if centers == -1:
            break
        # print(centers)
        if len(centers) > 2: 
            linears = finder.checkLinear(centers)
        if linears: equals = finder.checkEqualGap(linears)
        if equals:
            branch = finder.check_branch(equals,centers)
            # print(branch[0])
            if len(branch[0]) == 4:
                print(branch)
                draw(branch[0])
        linears.clear()
        equals.clear()
        branch.clear()
        
    
    


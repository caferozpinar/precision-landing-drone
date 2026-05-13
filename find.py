import cv2
import numpy as np
import time
import math
import warnings

warnings.filterwarnings("ignore")

threshold_branch = 20
threshold_lin = 25
threshold_eq_rat = 30

img = np.zeros((800,1920,3), dtype=np.uint8)

array = np.array([(450,300),(500,300),(550,300),(550,350),(550,400),(100,100),(200,200),(155,145)])
linear_points = []
equal_points = []

def distance(a,b):
    k = a[0] - b[0]
    l = a[1] - b[1]
    return math.sqrt((k*k)+(l*l))

#(0,255,255)
def check_branch():
    for i in range(len(equal_points)):
        lenx = abs(equal_points[i][0][0] - equal_points[i][2][0])
        leny = abs(equal_points[i][0][1] - equal_points[i][2][1])

        lenx = lenx + leny
        leny = lenx - leny
        lenx = lenx - leny
        lenx = - lenx

        aci = -math.degrees(math.atan2(equal_points[i][0][0] - equal_points[i][2][0], equal_points[i][0][1] - equal_points[i][2][1]))
        if aci > 90:
            xmin = equal_points[i][1][0] + lenx - threshold_branch
            xmax = equal_points[i][1][0] + lenx + threshold_branch
            ymin = equal_points[i][1][1] + leny - threshold_branch
            ymax = equal_points[i][1][1] + leny + threshold_branch

            cv2.circle(img, (xmin,ymin), radius=3, color=(255, 255, 255), thickness=1)
            cv2.circle(img, (xmax,ymax), radius=3, color=(255, 255, 255), thickness=1)
            cv2.circle(img, (xmin,ymax), radius=3, color=(255, 255, 255), thickness=1)
            cv2.circle(img, (xmax,ymin), radius=3, color=(255, 255, 255), thickness=1)
            
            for shrc in array:
                print
                if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                    cv2.line(img, equal_points[i][1], shrc, (0,0,255), 2)

            xmin = equal_points[i][1][0] - lenx - threshold_branch
            xmax = equal_points[i][1][0] - lenx + threshold_branch
            ymin = equal_points[i][1][1] - leny - threshold_branch
            ymax = equal_points[i][1][1] - leny + threshold_branch

            cv2.circle(img, (xmin,ymin), radius=3, color=(255, 255, 255), thickness=1)
            cv2.circle(img, (xmax,ymax), radius=3, color=(255, 255, 255), thickness=1)
            cv2.circle(img, (xmin,ymax), radius=3, color=(255, 255, 255), thickness=1)
            cv2.circle(img, (xmax,ymin), radius=3, color=(255, 255, 255), thickness=1)

            for shrc in array:
                print
                if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                    cv2.line(img, equal_points[i][1], shrc, (0,0,255), 2)

        else:
            xmin = equal_points[i][1][0] - lenx - threshold_branch
            xmax = equal_points[i][1][0] - lenx + threshold_branch
            ymin = equal_points[i][1][1] + leny - threshold_branch
            ymax = equal_points[i][1][1] + leny + threshold_branch

            cv2.circle(img, (xmin,ymin), radius=3, color=(255, 255, 255), thickness=1)
            cv2.circle(img, (xmax,ymax), radius=3, color=(255, 255, 255), thickness=1)
            cv2.circle(img, (xmin,ymax), radius=3, color=(255, 255, 255), thickness=1)
            cv2.circle(img, (xmax,ymin), radius=3, color=(255, 255, 255), thickness=1)

            for shrc in array:
                print
                if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                    cv2.line(img, equal_points[i][1], shrc, (0,0,255), 2)
            
            xmin = equal_points[i][1][0] + lenx - threshold_branch
            xmax = equal_points[i][1][0] + lenx + threshold_branch
            ymin = equal_points[i][1][1] - leny - threshold_branch
            ymax = equal_points[i][1][1] - leny + threshold_branch

            cv2.circle(img, (xmin,ymin), radius=3, color=(255, 255, 255), thickness=1)
            cv2.circle(img, (xmax,ymax), radius=3, color=(255, 255, 255), thickness=1)
            cv2.circle(img, (xmin,ymax), radius=3, color=(255, 255, 255), thickness=1)
            cv2.circle(img, (xmax,ymin), radius=3, color=(255, 255, 255), thickness=1)

            for shrc in array:
                print
                if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                    cv2.line(img, equal_points[i][1], shrc, (0,0,255), 2)
            
            

        

        
    cv2.imshow("test", img)


def check_mid(points):
    useds = []
    for i in range(len(points)):
        if (distance(points[i][0],points[i][1]) + distance(points[i][0],points[i][2])) <= (distance(points[i][1],points[i][0]) + distance(points[i][1],points[i][2])):
            if(distance(points[i][0],points[i][1]) + distance(points[i][0],points[i][2])) <= (distance(points[i][2],points[i][0]) + distance(points[i][2],points[i][1])):
                mid_p = points[i][0]
            else:
                mid_p = points[i][2]
        elif(distance(points[i][1], points[i][0]) + distance(points[i][1], points[i][2])) <= (distance(points[i][2], points[i][0]) + distance(points[i][2], points[i][1])):
            mid_p = points[i][1]
        else:
            mid_p = points[i][2]

        sortedPoints = [(0,0)] * 3
        allLocs = [0, 1, 2]
        foundLoc = points[i].index(mid_p)
        allLocs.remove(foundLoc)
        sortedPoints[0] = points[i][allLocs[0]]
        sortedPoints[1] = points[i][foundLoc]
        sortedPoints[2] = points[i][allLocs[1]]

        minLoc = sortedPoints.index(min(sortedPoints[0], sortedPoints[2]))
        if minLoc == 2:
            swapArr = [(0,0)]*3
            swapArr[0] = sortedPoints[2]
            swapArr[2] = sortedPoints[0]
            sortedPoints[0] = swapArr[0]
            sortedPoints[2] = swapArr[2]
        
        if sortedPoints in useds: continue
        useds.append(sortedPoints)

        threshold_eq = distance(mid_p, sortedPoints[0]) / 100 * threshold_eq_rat
        passVar = 0
        if abs(distance(mid_p, sortedPoints[0]) - distance(mid_p, sortedPoints[2])) < threshold_eq:
            cv2.line(img,sortedPoints[0], sortedPoints[2],(0,0,255),2)
            cv2.circle(img, sortedPoints[1], radius=3, color=(255, 0, 0), thickness=4)
            equal_points.insert(0, (sortedPoints[0], sortedPoints[1], sortedPoints[2]))
            passVar = 1
        else:
            cv2.line(img, sortedPoints[0], sortedPoints[2], (255,255,255), 2)
            cv2.circle(img, mid_p, radius=3, color=(255, 0, 255), thickness=4)
    

def check_diagonal():
    global img
    img = np.zeros((800,1920,3), dtype=np.uint8)
    #print("linear array 0 = ")
    
    #print(linear_points)
    #print(array)
    #print(len(array))
    #print("check arrays")



    for i in range(len(array)):
        #verilen koordinatlara yeşil noktalar çizdik
        img = cv2.circle(img, array[i], radius=3, color=(0, 255, 0), thickness=4)
        for j in range(i+1,len(array)):
            # iki noktası bilinen doğru denklemi
            # ilk olarak m'i bulmalıyız
            y = array[i][1] - array[j][1]
            x = array[i][0] - array[j][0]

            m = y / x
            b = array[i][1] - (m*array[i][0])
            for k in range(len(array)):
                if k != i and k != j :
                    x = array[k][0]
                    y = array[k][1]

                    
                    estx = x
                    if m: estx = (y - b) / m

                    esty = m*x + b
                    if math.isinf(m): 
                        esty = y
                        estx = array[i][0]
                    if math.isnan(m): esty = y

                    result_y = esty - y
                    result_x = estx - x
                    result_x = abs(result_x)
                    result_y = abs(result_y)
                    
                    if result_x < threshold_lin and result_y < threshold_lin:
                        jus = 250
                        if distance(array[i],array[j]) < jus and distance(array[i],array[k]) < jus and distance(array[k],array[j]) < jus:
                            linear_points.insert(0,((array[i][0],array[i][1]),(array[j][0],array[j][1]),(array[k][0],array[k][1])))
                            cv2.line(img,array[i],array[j],(255,0,0),2)
                            cv2.line(img,array[i],array[k],(255,0,0),2)
                            cv2.line(img,array[k],array[j],(255,0,0),2)

   


def click_event(event, x, y, flags, params):
    global array
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        array = np.vstack([array,[x, y]])
        #print(array)
        check_diagonal()
        check_mid(linear_points)
        check_branch()
    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.destroyAllWindows()
        



check_diagonal()
check_mid(linear_points)
check_branch()
cv2.setMouseCallback('test', click_event)
    


k = cv2.waitKey(0)
if k:
    cv2.destroyAllWindows()

        
        



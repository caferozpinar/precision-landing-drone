import Parameters as p
import numpy as np
import math
import cv2

def Color(returnType: str, frame: list):
    """Applies Threshold to given image (%50-%50) and turns it to 
    black and white image. returns it as points or binary (0-255) frame 

    PARAMETERS

    returnType (str): Can be set as 

    ``FRAME`` or ``POINTS``

    ``FRAME``: Set return type to binary image frame\n
    ``POINTS``: Set return type to points array\n

    frame: (``cv2.MAT``) object.

    out: ``frame`` or ``points``:
    
    ``frame``: Frame out of binary image 
    ``points``: Array of detected white point centers
    """
    try:
        imageGrayScale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        (thresh, imageBinary) = cv2.threshold(imageGrayScale, 198, 255, cv2.THRESH_BINARY)
    except Exception as e:
        return []


    if returnType == "POINTS":
        arrayPoints = []
        _ , contours, _ = cv2.findContours(imageBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for i in contours:
            x, y, width, height = cv2.boundingRect(i)
            x += width/2
            y += height/2
            arrayPoints.append((x, y))
            x, y = 0, 0
        
        return arrayPoints

    if returnType == "FRAME":
        return imageBinary

def Blob(frame):
    """Finds blobs on given frame and return blob centers array

    PARAMETERS

    frame ``cv2.MAT`` object:

    out: ``points``:

    ``points``: Array of detected white points center
    """
    dtector = cv2.SimpleBlobDetector_create()
    # Detect blobs.
    keypoints1 = dtector.detect(frame)
    frame = np.invert(frame)
    keypoints2 = dtector.detect(frame)
    keypoints = keypoints1 + keypoints2
    pts = []
    for i in keypoints:
        x, y = i.pt
        pts.append((int(x),int(y)))
    return pts

def __distance(point1, point2):
    return math.sqrt(((point1[0] - point2[0]) * (point1[0] - point2[0])) + ((point1[1] - point2[1]) * (point1[1] - point2[1])))

def Marker(pointsArray : list, shape : str = "T"):
    if shape == "BASIC":
        temp_x = 0
        temp_y = 0
        if pointsArray == []:
            return []
        else:
            for i in pointsArray:
                temp_x += (i[0] / len(pointsArray))
                temp_y += (i[1] / len(pointsArray))
            a = []
            if temp_x == 0 and temp_y == 0:
                return []
            a.append(((temp_x, temp_y), (temp_x, temp_y), (temp_x, temp_y), (temp_x, temp_y)))
            return a
        
    if shape == "T":
        if len(pointsArray) < 4:
            return []
        # phase 1 for detecting T shape.
        # finds 3 points looks linear
        markerPoints = []
        for point_1 in pointsArray:
            for point_2 in pointsArray:
                if point_1 == point_2: continue
                if point_1[0] == point_2[0]:
                     enable_x = True
                     enable_y = False
                elif point_1[1] == point_2[1]:
                     enable_x = False
                     enable_y = True
                else:
                    enable_x = True
                    enable_y = True
                    slope = (point_1[1] - point_2[1]) / (point_1[0] - point_2[0])
                    intercept = point_1[1] - (point_1[0] * slope)
                for point_3 in pointsArray:
                    if point_3 == point_1 or point_3 == point_2 : continue
                    
                    elif enable_x and not enable_y:
                        estimated_x = point_1[0]
                        estimated_y = point_3[1]
                            
                    elif enable_y and not enable_x:
                        estimated_x = point_3[0]
                        estimated_y = point_1[1]
                        
                    else:
                        estimated_x = (point_3[1] - intercept) / slope
                        estimated_y = slope * point_3[0] + intercept
                        
                    # calculate error_x and error_y
                    # error x = estimated_x - x
                    error = __distance((estimated_x, estimated_y), point_3)
                    if error <= __distance(point_1, point_2) * 0.1:
                        if abs(__distance(point_1, point_2) - __distance(point_2, point_3)) <= __distance(point_1, point_2) * 0.1 and __distance(point_1, point_3) > __distance(point_1, point_2):
                            pointsArray.remove(point_1)
                            pointsArray.remove(point_2)
                            pointsArray.remove(point_3)
                            for point_4 in pointsArray:
                                if abs(__distance(point_1, point_4) - __distance(point_3, point_4)) <= __distance(point_1, point_2) * 0.2:
                                    if abs((__distance(point_1, point_2) * 1.5) - __distance(point_2, point_4)) <= __distance(point_1, point_2) * 0.2:
                                        markerPoints.append((point_1, point_2, point_3, point_4))
        return markerPoints
    if shape == "square":
        # Not written yet no need for now may be complete later
        pass





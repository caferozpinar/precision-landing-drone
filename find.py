######################################################################################################################################
# Python Cartessian Coordinate System "T" Shape Detect Algorithm Module
# Version : 0.2.2
# Author : Cafer Umut Ozpinar
# Date : 02.12.2022
# Note : ...
######################################################################################################################################
import math
import numpy as np

class find_T():

    def __init__(self, linear_threshold = 10.0, gap_threshold=3.0, branch_threshold = 4.0):

        self.branch_threshold = branch_threshold    # T shape's branch detect threshold 
        self.linear_threshold = linear_threshold    # Detection threshold of T shaped linear three-point
        self.gap_threshold = gap_threshold          # Equal gap detection threshold at three points of T shape
        # self.array = np.array([(-1, -1),(-1, -1),(-1, -1)])
        self.linear_points = []
        self.equal_gap_points = []
    
    def distance(self,a, b):

        #calculate distance between a - b coordinates (dst^2 = (x1 - x2)^2 + (y1 - y2)^2)
        return math.sqrt(((a[0] - b[0]) * (a[0] - b[0])) + ((a[1] - b[1]) * (a[1] - b[1])))


    # 3 point linear detect function
    def checkLinear(self,array):

        for point_1 in range(len(array)):
            for point_2 in range(point_1 + 1, len(array)):

                # line equation with two known points => y = mx + b
                # m = y1 - y2 / x1 - x2
                # b = y - mx
                tempx = (array[point_1][1] - array[point_2][1])
                tempy = (array[point_1][0] - array[point_2][0])
                if tempx == 0 or tempy == 0:
                    continue
                m = tempx / tempy
                b = array[point_1][1] - (m * array[point_1][0])

                for point_3 in range(len(array)):

                    if point_3 == point_1 or point_3 == point_2 : continue
                    
                    # if m = 0 => x / 0 = undefined
                    # for fix this if m = 0 estimated_x = x
                    estimated_x = array[point_3][0]
                    if m: estimated_x = (array[point_3][1] - b) / m

                    # if x1 - x2 = 0 => m = NaN or inf
                    # for fix this if m = NaN or inf estimated_y = y and 
                    estimated_y = m * array[point_3][0] + b
                    if math.isinf(m) or math.isnan(m): 
                        estimated_y = array[point_1][1]
                        estimated_x = array[point_1][0]
                    
                    # calculate error_x and error_y 
                    # error x = estimated_x - x
                    error_x = abs(estimated_x - array[point_3][0])
                    error_y = abs(estimated_y - array[point_3][1])

                    if error_x < self.distance(array[point_1],array[point_2]) / self.linear_threshold and error_y < self.distance(array[point_1],array[point_2]) / self.linear_threshold:
                        # linear points list => ((x1,y1),(x2,y2),(x3,y3))
                        self.linear_points.insert(0,((array[point_1][0],array[point_1][1]),(array[point_2][0],array[point_2][1]),(array[point_3][0],array[point_3][1])))
                        
        return self.linear_points

    # 3 point equal gap detect function
    def checkEqualGap(self,points):
        useds = []
        for i in range(len(points)):
            if (self.distance(points[i][0],points[i][1]) + self.distance(points[i][0],points[i][2])) <= (self.distance(points[i][1],points[i][0]) + self.distance(points[i][1],points[i][2])):
                if(self.distance(points[i][0],points[i][1]) + self.distance(points[i][0],points[i][2])) <= (self.distance(points[i][2],points[i][0]) + self.distance(points[i][2],points[i][1])):
                    mid_p = points[i][0]
                else:
                    mid_p = points[i][2]
            elif(self.distance(points[i][1], points[i][0]) + self.distance(points[i][1], points[i][2])) <= (self.distance(points[i][2], points[i][0]) + self.distance(points[i][2], points[i][1])):
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
            threshold_value = int(self.distance(mid_p, sortedPoints[0]) / self.gap_threshold)
            
            if abs(self.distance(sortedPoints[1], sortedPoints[0]) - self.distance(sortedPoints[1], sortedPoints[2])) < threshold_value:
                self.equal_gap_points.insert(0, (sortedPoints[0], sortedPoints[1], sortedPoints[2]))
        return self.equal_gap_points


    # check T shape's branch
    def check_branch(self,equal_points,array):

        for i in range(len(equal_points)):
            lenx = abs(equal_points[i][0][0] - equal_points[i][2][0])
            leny = abs(equal_points[i][0][1] - equal_points[i][2][1])
            dst = self.distance(equal_points[i][0],equal_points[i][1])

            lenx = lenx + leny
            leny = lenx - leny
            lenx = lenx - leny
            lenx = - lenx

            aci = -math.degrees(math.atan2(equal_points[i][0][0] - equal_points[i][2][0], equal_points[i][0][1] - equal_points[i][2][1]))
            if aci > 90:
                xmin = int((equal_points[i][1][0] + lenx) - (dst/self.branch_threshold))
                xmax = int((equal_points[i][1][0] + lenx) + (dst/self.branch_threshold))
                ymin = int((equal_points[i][1][1] + leny) - (dst/self.branch_threshold))
                ymax = int((equal_points[i][1][1] + leny) + (dst/self.branch_threshold))
                
                for shrc in array:
                    if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                        equal_points[i] = list(equal_points[i])
                        templist = shrc[0],shrc[1]
                        equal_points[i].insert(3,templist)

                xmin = int((equal_points[i][1][0] - lenx) - (dst/self.branch_threshold))
                xmax = int((equal_points[i][1][0] - lenx) + (dst/self.branch_threshold))
                ymin = int((equal_points[i][1][1] - leny) - (dst/self.branch_threshold))
                ymax = int((equal_points[i][1][1] - leny) + (dst/self.branch_threshold))

                for shrc in array:
                    if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                        equal_points[i] = list(equal_points[i])
                        templist = shrc[0],shrc[1]
                        equal_points[i].insert(3,templist)

            else:
                xmin = int((equal_points[i][1][0] - lenx) - (dst/self.branch_threshold))
                xmax = int((equal_points[i][1][0] - lenx) + (dst/self.branch_threshold))
                ymin = int((equal_points[i][1][1] + leny) - (dst/self.branch_threshold))
                ymax = int((equal_points[i][1][1] + leny) + (dst/self.branch_threshold))

                for shrc in array:
                    if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                        equal_points[i] = list(equal_points[i])
                        templist = shrc[0],shrc[1]
                        equal_points[i].insert(3,templist)

                xmin = int((equal_points[i][1][0] + lenx) - (dst/self.branch_threshold))
                xmax = int((equal_points[i][1][0] + lenx) + (dst/self.branch_threshold))
                ymin = int((equal_points[i][1][1] - leny) - (dst/self.branch_threshold))
                ymax = int((equal_points[i][1][1] - leny) + (dst/self.branch_threshold))

                for shrc in array:
                    if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                        equal_points[i] = list(equal_points[i])
                        templist = shrc[0],shrc[1]
                        equal_points[i].insert(3,templist)
        return equal_points
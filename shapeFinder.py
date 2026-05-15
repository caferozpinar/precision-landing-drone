
import math



class TFinder():
    
    def __init__(self):
        self.branch_threshold = 0.0
        self.linear_threshold = 0.0
        self.gap_threshold = 0.0
        print("Finder initilaziton --DONE--")
    
    def setThreshold(self, linear_threshold = 0.0, gap_threshold = 0.0, branch_threshold = 0.0):
        self.linear_threshold = linear_threshold
        self.branch_threshold = branch_threshold
        self.gap_threshold = gap_threshold
        print("Finder threshold set --DONE--")
        print("Linear threshold value : " + str(linear_threshold))
        print("Gap threshold value : " + str(gap_threshold))
        print("Branch threshold value : " + str(branch_threshold))

    def distance(self, point1, point2):
        #calculate distance between point1 - point2 coordinates (dst^2 = (x1 - x2)^2 + (y1 - y2)^2)
        return math.sqrt(((point1[0] - point2[0]) * (point1[0] - point2[0])) + ((point1[1] - point2[1]) * (point1[1] - point2[1])))

    def calculateROI(self,Tshape):
        min_x = Tshape[0][0]
        min_y = Tshape[0][1]
        max_x = Tshape[0][0]
        max_y = Tshape[0][1]

        for arr in Tshape:
            if arr[0] < min_x : min_x = arr[0]
            if arr[1] < min_y : min_y = arr[1]
            if arr[0] > max_x : max_x = arr[0]
            if arr[1] > max_y : max_y = arr[1]

        height = max_y - min_y
        width = max_x - min_x
        

        return int(min_x), int(min_y), int(width), int(height)


    def findShape(self,array):
        shape_array = []
        shape_array.clear()

        linear_centers = []
        linear_centers.clear()

        equal_linears = []
        equal_linears.clear()

        if len(array) < 2:
            return shape_array

        linear_centers = self.checkLinear(array)
        equal_linears = self.checkEqual(linear_centers)
        shape_array = self.checkBranch(equal_linears,array)
        
        if len(shape_array) < 4:
            shape_array.clear()
            return 0, shape_array

        return 1, shape_array

    def checkLinear(self, array):
        linear_points = []
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

                    if error_x < self.distance(array[point_1], array[point_2]) / self.linear_threshold and error_y < self.distance(array[point_1], array[point_2]) / self.linear_threshold:
                        # linear points list => ((x1,y1),(x2,y2),(x3,y3))
                        linear_points.insert(0, ((array[point_1][0], array[point_1][1]), (array[point_2][0], array[point_2][1]), (array[point_3][0], array[point_3][1])))
                        
        return linear_points

    def checkEqual(self, array):
        useds = []
        equal_linears = []
        equal_linears.clear()

        for i in range(len(array)):
            if (self.distance(array[i][0], array[i][1]) + self.distance(array[i][0], array[i][2])) <= (self.distance(array[i][1], array[i][0]) + self.distance(array[i][1], array[i][2])):
                if(self.distance(array[i][0], array[i][1]) + self.distance(array[i][0], array[i][2])) <= (self.distance(array[i][2], array[i][0]) + self.distance(array[i][2], array[i][1])):
                    mid_p = array[i][0]
                else:
                    mid_p = array[i][2]
            elif(self.distance(array[i][1], array[i][0]) + self.distance(array[i][1], array[i][2])) <= (self.distance(array[i][2], array[i][0]) + self.distance(array[i][2], array[i][1])):
                mid_p = array[i][1]
            else:
                mid_p = array[i][2]

            sortedarray = [(0,0)] * 3
            allLocs = [0, 1, 2]
            foundLoc = array[i].index(mid_p)
            allLocs.remove(foundLoc)
            sortedarray[0] = array[i][allLocs[0]]
            sortedarray[1] = array[i][foundLoc]
            sortedarray[2] = array[i][allLocs[1]]

            minLoc = sortedarray.index(min(sortedarray[0], sortedarray[2]))
            if minLoc == 2:
                swapArr = [(0,0)]*3
                swapArr[0] = sortedarray[2]
                swapArr[2] = sortedarray[0]
                sortedarray[0] = swapArr[0]
                sortedarray[2] = swapArr[2]
            
            
            if sortedarray in useds: continue
            useds.append(sortedarray)
            threshold_value = int(self.distance(mid_p, sortedarray[0]) / self.gap_threshold)
            
            if abs(self.distance(sortedarray[1], sortedarray[0]) - self.distance(sortedarray[1], sortedarray[2])) < threshold_value:
                equal_linears.insert(0, (sortedarray[0], sortedarray[1], sortedarray[2]))

        return equal_linears

    def checkBranch(self, equal_linears,array):
        shape_array = []
        shape_array.clear
        shape_array = equal_linears
        if len(equal_linears) == 1: shape_array = equal_linears[0]
        shape_array = list(shape_array)

        for i in range(len(equal_linears)):
            lenx = abs(equal_linears[i][0][0] - equal_linears[i][2][0])
            leny = abs(equal_linears[i][0][1] - equal_linears[i][2][1])
            dst = self.distance(equal_linears[i][0],equal_linears[i][1])

            lenx = lenx + leny
            leny = lenx - leny
            lenx = lenx - leny
            lenx = - lenx

            aci = -math.degrees(math.atan2(equal_linears[i][0][0] - equal_linears[i][2][0], equal_linears[i][0][1] - equal_linears[i][2][1]))
            if aci > 90:
                xmin = int((equal_linears[i][1][0] + lenx) - (dst / self.branch_threshold))
                xmax = int((equal_linears[i][1][0] + lenx) + (dst / self.branch_threshold))
                ymin = int((equal_linears[i][1][1] + leny) - (dst / self.branch_threshold))
                ymax = int((equal_linears[i][1][1] + leny) + (dst / self.branch_threshold))
                for shrc in array:
                    if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                        templist = shrc[0], shrc[1]
                        shape_array.insert(3, templist)

                xmin = int((equal_linears[i][1][0] - lenx) - (dst / self.branch_threshold))
                xmax = int((equal_linears[i][1][0] - lenx) + (dst / self.branch_threshold))
                ymin = int((equal_linears[i][1][1] - leny) - (dst / self.branch_threshold))
                ymax = int((equal_linears[i][1][1] - leny) + (dst / self.branch_threshold))

                for shrc in array:
                    if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                        templist = shrc[0], shrc[1]
                        shape_array[i].insert(3, templist)

            else:
                xmin = int((equal_linears[i][1][0] - lenx) - (dst / self.branch_threshold))
                xmax = int((equal_linears[i][1][0] - lenx) + (dst / self.branch_threshold))
                ymin = int((equal_linears[i][1][1] + leny) - (dst / self.branch_threshold))
                ymax = int((equal_linears[i][1][1] + leny) + (dst / self.branch_threshold))

                for shrc in array:
                    if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                        templist = shrc[0], shrc[1]
                        shape_array[i].insert(3, templist)

                xmin = int((equal_linears[i][1][0] + lenx) - (dst / self.branch_threshold))
                xmax = int((equal_linears[i][1][0] + lenx) + (dst / self.branch_threshold))
                ymin = int((equal_linears[i][1][1] - leny) - (dst / self.branch_threshold))
                ymax = int((equal_linears[i][1][1] - leny) + (dst / self.branch_threshold))

                for shrc in array:
                    if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                        templist = shrc[0], shrc[1]
                        shape_array[i].insert(3, templist)

        return shape_array
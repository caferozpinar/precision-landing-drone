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
        girx = point1[0] - point2[0]
        giry = point1[1] - point2[1]
        if not giry: return girx
        if not girx: return giry
        return math.sqrt((girx ** 2) + (giry ** 2))
    
    #def distance_old(self, point1, point2):
        #calculate distance between point1 - point2 coordinates (dst^2 = (x1 - x2)^2 + (y1 - y2)^

        
        #return ((point1[0] - point2[0]) * 0.35) + (point1[1] - point2[1])

    def calculateROI(self,Tshape):
        min_x = Tshape[0][0][0]
        min_y = Tshape[0][0][1]
        max_x = Tshape[0][0][0]
        max_y = Tshape[0][0][1]

        for arr in Tshape[0]:
            if arr[0] < min_x : min_x = arr[0]
            if arr[1] < min_y : min_y = arr[1]
            if arr[0] > max_x : max_x = arr[0]
            if arr[1] > max_y : max_y = arr[1]

        height = max_y - min_y
        width = max_x - min_x
        

        return int(min_x), int(min_y), int(width), int(height)


    def findShape(self, array):
        print(array)
        shape_array = []
        shape_array.clear()

        linear_centers = []
        linear_centers.clear()

        equal_olmayan = []
        equal_olmayan.clear()
        if len(array) < 2:
            return 2, shape_array

        linear_centers = self.checkLinear(array)
        equal_olmayan = self.checkEqual(linear_centers)
        shape_array = self.checkBranch(equal_olmayan,array)
        if len(shape_array) >= 1:
            shape_array = list(shape_array)
            tmp = shape_array[0]
            shape_array.clear()
            shape_array = tmp
        if len(shape_array) < 4:
            shape_array = list(len(shape_array))
            print("what")
            shape_array.clear()
            return 2, shape_array
        return 0, shape_array

    def checkLinear(self, array):
        linear_points = []
        for point_1 in range(len(array) - 1):
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

                for point_3 in array:

                    if point_3 == array[point_1] or point_3 == array[point_2] : continue
                    
                    # if m = 0 => x / 0 = undefined
                    # for fix this if m = 0 estimated_x = x
                    estimated_x = point_3[0]
                    if m: estimated_x = (point_3[1] - b) / m

                    # if x1 - x2 = 0 => m = NaN or inf
                    # for fix this if m = NaN or inf estimated_y = y and 
                    estimated_y = m * point_3[0] + b
                    if math.isinf(m) or math.isnan(m): 
                        estimated_y = array[point_1][1]
                        estimated_x = array[point_1][0]
                    
                    # calculate error_x and error_y 
                    # error x = estimated_x - x
                    error_x = abs(estimated_x - point_3[0])
                    error_y = abs(estimated_y - point_3[1])

                    if error_x < self.distance(array[point_1], array[point_2]) / self.linear_threshold and error_y < self.distance(array[point_1], array[point_2]) / self.linear_threshold:
                        # linear points list => ((x1,y1),(x2,y2),(x3,y3))
                        linear_points.insert(0, ((array[point_1][0], array[point_1][1]), (array[point_2][0], array[point_2][1]), (point_3[0], point_3[1])))
                        
        return linear_points

    def checkEqual(self, array):
        useds = []
        equal_olmayan = []
        equal_olmayan.clear()

        for rei in array:
            if (self.distance(rei[0], rei[1]) + self.distance(rei[0], rei[2])) <= (self.distance(rei[1], rei[0]) + self.distance(rei[1], rei[2])):
                if(self.distance(rei[0], rei[1]) + self.distance(rei[0], rei[2])) <= (self.distance(rei[2], rei[0]) + self.distance(rei[2], rei[1])):
                    mid_p = rei[0]
                else:
                    mid_p = rei[2]
            elif(self.distance(rei[1], rei[0]) + self.distance(rei[1], rei[2])) <= (self.distance(rei[2], rei[0]) + self.distance(rei[2], rei[1])):
                mid_p = rei[1]
            else:
                mid_p = rei[2]

            sortedarray = [(0,0)] * 3
            allLocs = [0, 1, 2]
            foundLoc = rei.index(mid_p)
            allLocs.remove(foundLoc)
            sortedarray[0] = rei[allLocs[0]]
            sortedarray[1] = rei[foundLoc]
            sortedarray[2] = rei[allLocs[1]]

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
                equal_olmayan.insert(0, (sortedarray[0], sortedarray[1], sortedarray[2]))

        return equal_olmayan

    def checkBranch(self, equal_linears, array):
        shape_array = []
        shape_array.clear()
        if not len(equal_linears): return shape_array
        shape_array = equal_linears
        iiii=-1

        for rika in equal_linears:
            iiii = iiii + 1
            rikabirsifir = rika[1][0]
            rikabirbir = rika[1][1]
            lenx = abs(rika[0][0] - rika[2][0])
            leny = abs(rika[0][1] - rika[2][1])
            dst = self.distance(rika[0],rika[1])

            lenx = lenx + leny
            leny = lenx - leny
            lenx = lenx - leny
            lenx = - lenx

            aci = -math.degrees(math.atan2(rika[0][0] - rika[2][0], rika[0][1] - rika[2][1]))
            if aci > 90:
                xmin = int((rikabirsifir + lenx) - (dst / self.branch_threshold))
                xmax = int((rikabirsifir + lenx) + (dst / self.branch_threshold))
                ymin = int((rikabirbir + leny) - (dst / self.branch_threshold))
                ymax = int((rikabirbir + leny) + (dst / self.branch_threshold))
                for shrc in array:
                    if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                        templist = shrc[0], shrc[1]
                        shape_array[iiii] = list(shape_array[iiii])
                        shape_array[iiii].insert(3, templist)

                xmin = int((rikabirsifir - lenx) - (dst / self.branch_threshold))
                xmax = int((rikabirsifir - lenx) + (dst / self.branch_threshold))
                ymin = int((rikabirbir - leny) - (dst / self.branch_threshold))
                ymax = int((rikabirbir - leny) + (dst / self.branch_threshold))

                for shrc in array:
                    if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                        templist = shrc[0], shrc[1]
                        shape_array[iiii] = list(shape_array[iiii])
                        shape_array[iiii].insert(3, templist)

            else:
                xmin = int((rikabirsifir - lenx) - (dst / self.branch_threshold))
                xmax = int((rikabirsifir - lenx) + (dst / self.branch_threshold))
                ymin = int((rikabirbir + leny) - (dst / self.branch_threshold))
                ymax = int((rikabirbir + leny) + (dst / self.branch_threshold))

                for shrc in array:
                    if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                        templist = shrc[0], shrc[1]
                        shape_array[iiii] = list(shape_array[iiii])
                        shape_array[iiii].insert(3, templist)

                xmin = int((rikabirsifir + lenx) - (dst / self.branch_threshold))
                xmax = int((rikabirsifir + lenx) + (dst / self.branch_threshold))
                ymin = int((rikabirbir - leny) - (dst / self.branch_threshold))
                ymax = int((rikabirbir - leny) + (dst / self.branch_threshold))

                for shrc in array:
                    if shrc[0] < xmax and shrc[0] > xmin and shrc[1] < ymax and shrc[1] > ymin:
                        templist = shrc[0], shrc[1]
                        shape_array[iiii] = list(shape_array[iiii])
                        shape_array[iiii].insert(3, templist)

        return shape_array

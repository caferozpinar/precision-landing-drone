import numpy as np
import math
from Encrypt import encrypt

class calculator:

    def __init__(self):
        pass

    def ROI(self,centers):
        leftupcorner = encrypt()
        rightdowncorner = encrypt()
        xmin = centers[0][0]
        xmax = centers[0][0]
        ymin = centers[0][1]
        ymax = centers[0][1]
        for x in range(len(centers)):
                if centers[x].any() != 0 :
                    if xmin > centers[x][0]:
                        xmin = centers[x][0]
                    
                    if xmax < centers[x][0]:
                        xmax = centers[x][0]

                    if ymin > centers[x][1]:
                        ymin = centers[x][1]

                    if ymax < centers[x][1]:
                        ymax = centers[x][1]

        leftupcorner.x = xmin
        leftupcorner.y = ymin

        rightdowncorner.x = xmax
        rightdowncorner.y = ymax

        width = abs(leftupcorner.x-rightdowncorner.x)
        height = abs(leftupcorner.y-rightdowncorner.y)

        return leftupcorner.x ,leftupcorner.y ,width ,height
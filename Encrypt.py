import math

class encrypt:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def set(self,x,y):
        self.x = x
        self.y = y

    def distance2(self,point):
        return math.sqrt(( (self.x-point.x)*(self.x-point.x) ) + ( (self.y-point.y)*(self.y-point.y) ))
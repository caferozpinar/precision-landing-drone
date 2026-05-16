import math
import time
import numpy
val = 765
cycle = 100000000

def fassqrt(val):
    
    # find highest bit
    highest = 1
    sqrt_highest = 1
    while highest < val:
        highest <<= 2
        sqrt_highest <<= 1

    val /= highest+0.0

    result = (val/4) + 1
    result = (result/2) + (val/(result*2))
    result = (result/2) + (val/(result*2))

    return result*sqrt_highest


def numpali():
    array = numpy.array([1, 5, 8, 12], dtype='i4')
    for i in range(cycle):
        c = array[0] + array[2]

def listsiz():
    array = [1, 5, 8, 12]
    for i in range(cycle):
        c = array[0] + array[2]

if __name__ == "__main__":
    t = time.time()
    numpali()
    print(time.time() - t)
    pass
    # b = math.sqrt(val)
    # print(a,b)

import time

a = 515
b = 712

d = 512
e = 712

cycle = 500000
array_g = ((1, 2),(3, 4),(1, 2),(5, 6))
def farkli():
    temp = 0
    for i in range(cycle):
        if a == b: # farklı değer karşılaştırma
            temp = 1

def ayni():
    temp = 0
    for i in range(cycle):
        if a == d:
            temp = 1

def aynilik():
    temp = 0
    for i in range(cycle):
        if not a == e:
            temp = 1

def farklisin():
    temp = 0
    toplam = 0
    for i in range(cycle):
        toplam = a - b
        temp = 1

def aynisin(array):
    temp = 0
    toplam = 0
    for i in range(cycle):
        toplam = array[0][0] - array[0][1]
        temp = 1

def fopii():
    temp = 0
    for b in range(cycle):
        for i in range(len(array_g)):
            for j in range(len(array_g)):
                for k in range(1):
                    if k == j or k == i: continue
                    temp = temp + 1

def fopi():
    temp = 0
    for b in range(cycle):
        for i in range(len(array_g)):
            for j in range(len(array_g)):
                for k in range(0):
                    pass
def foci(array):
    for b in range(cycle):
        for i in range(len(array)):
            temp = array_g[i][0]
if __name__ == "__main__":
    #array = ((512, 512),(512, 512))
    tim = time.time()
    fopii()
    print(time.time() - tim)
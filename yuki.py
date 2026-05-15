array = ((1, 2),(3, 4),(5, 6),(7, 8))

lenarr = len(array)
          
for point_1 in range(len(array) - 1):
    #print(point_1, len(array))
    for point_2 in range(point_1 + 1, len(array)):
        #print(array[point_1], array[point_2])
        for point_3 in array:
            if point_3 == array[point_1] or point_3 == array[point_2]:
                print(array[point_1], array[point_2], point_3)
            pass
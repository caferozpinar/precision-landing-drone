def trackCoordinates(coor_array):
    
    mid_pointer_x = (coor_array[0][0] + coor_array[2][0]) / 2
    mid_pointer_y = (coor_array[0][1] + coor_array[2][1]) / 2
    print(mid_pointer_y, mid_pointer_x)

coor_array = ((3, 7) , (7, 9), (7, 9), (7, 9))



trackCoordinates(coor_array)
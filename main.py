
import cam
import shapeFinder

def stage(phase = 1):
    # Phase " 1 " set threshold and initalize system
    if phase == 1:
        global camera
        global TFinder
        # Open camera and detect shape/color
        camera = cam.colorDetect()
        camera.captureCam("C:/Users/ozpin/Documents/My_Workspace/TEKNOFEST-2023/SERBEST-GÖREV/Precision_land_software/DRONE SOFTWARE/versions/ver_0.3.0/test.mp4")
        camera.setThreshold((0, 0, 169), (179, 34, 255))
        camera.initTracker("kcf")
        TFinder = shapeFinder.TFinder()
        TFinder.setThreshold(10.0, 3.0, 1.5)
        return 2

    # Read next frame and detect objects
    if phase == 2:
        global centers
        success, centers = camera.detect()

        if success == 1 : return 3
        elif success == 2 : return 2
        # elif success == 3 : return 1
        else : return -1

    # detect object in frame
    if phase == 3:
        global Tshape
        # Finding interested shape in returned centers
        success, Tshape = TFinder.findShape(centers)
        if success == 1 : return 4
        elif success == 0: return 2
        else : return -1

    # Track Region of interest
    if phase == 4:
        roi = TFinder.calculateROI(Tshape)
        success = camera.roiTracker(roi, True)

        if success == 2: return 2
        if success == 3: return 2
        if success == 4: return 3



    else :
        print("Undefined ERROR")
        print("Flight mode set RTL")
        rtl = 1
        if not rtl :
            latitude , longitude = 1, 2
            print("rtl failed! landing imadietly")
            print("Emergency landing coordinates :")
            print("Latitude : " + str(latitude))
            print("Longitude : " + str(longitude))
        return 6730
        




if __name__ == "__main__":

    print("################### Starting Script ###################")
    value = 1
    while 1:
        value = stage(value)

        if value == 6730 :
            print("SCRIPT EXITED WITH CODE 6730")
            break
    print("################### END OF SCRIPT ####################")

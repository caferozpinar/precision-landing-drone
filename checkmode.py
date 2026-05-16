import shapeFinder

centers =[(639.5, 240.0), (386.5, 146.0), (380.5, 272.5), (150.0, 278.0), (377.5, 393.5)]

finder_threshold = 5.0, 3.0, 2.0
print(finder_threshold)
TFinder = shapeFinder.TFinder()
TFinder.setThreshold(finder_threshold[0], finder_threshold[1], finder_threshold[2])
success, Tshape = TFinder.findShape(centers)
print("Tshape = " + str(Tshape))
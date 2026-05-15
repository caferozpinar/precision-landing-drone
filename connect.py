import dronekit
import sys
import cv2
import numpy as np

size = 450, 450, 3
map = np.zeros(size, dtype=np.uint8)

connection_string = sys.argv[1]
print(connection_string)
vehicle = dronekit.connect(connection_string, wait_ready=True)

print(vehicle._location.global_relative_frame)
cv2.imshow("test", map)

while True:
    k = cv2.waitKey(1) & 0xff
    if k == 27 :
        cv2.destroyAllWindows()
        break
import cv2
import dronekit

vhc = dronekit.connect()

frame = cv2.imread("acik.png")

hsvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
maskedimage = cv2.inRange(hsvimage, (0, 0, 169), (179, 84, 255))

cv2.imshow("uhaa", frame)
cv2.imshow("hebelehübele", maskedimage)

cv2.waitKey(0)
cv2.destroyAllWindows()

vhc.command.upload
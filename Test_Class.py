import Detect
import cv2
import numpy as np

frame = cv2.imread("../../../Data_Files/Image_Saves/black.png") 

Detect.Color("POINTS", frame)
import numpy as np
import time
import cv2
import cv2.aruco as aruco
#读取图片
frame=cv2.imread('./LINEMOD/a1.jpg')
#调整图片大小
frame=cv2.resize(frame,None,fx=0.2,fy=0.2,interpolation=cv2.INTER_CUBIC)
#灰度话
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#设置预定义的字典
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)
corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
#画出标志位置
aruco.drawDetectedMarkers(frame, corners,ids)


cv2.imshow("frame",frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

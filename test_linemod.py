import cv2
import os
import matplotlib.pyplot as plt
# 存储少于2个ARUCO标记的图像文件名
images_to_delete = []
depth_to_delete = []

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

# corners, ids, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)

# 遍历指定文件夹中的所有图像文件
folder_path = ('./LINEMOD/ob4/JPEGImages')# 4,
# depth_folder = './LINEMOD/ob/depth'
num_bad = 0
num_failload = 0
num_all = 0
for filename in os.listdir(folder_path):
    num_all += 1
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):  # 检查文件扩展名
        # 读取图像
        image = cv2.imread(os.path.join(folder_path, filename))
        if image is not None:
            # 检测图像中的ARUCO标记
            corners, ids, _ = detector.detectMarkers(image)
            # 如果检测到的标记数量小于2个，打印文件名
            if ids is None:
                print(f'Image with less than 2 ArUco markers: {filename}')
                images_to_delete.append(filename)
                num_bad += 1
            elif ids is not None:
                if len(ids) < 2:
                    print(f'Image with less than 2 ArUco markers: {filename}')
                    images_to_delete.append(filename)
                    num_bad += 1
        else:
            print(f'Failed to load image: {filename}')
            num_failload += 1


print(f'Number of images with less than 2 ArUco markers: {num_bad}')
print(f'Number of failed to load images: {num_failload}')
print(f'percent: {num_bad/num_all}')

# 绘制饼状图
labels = ['qualified image:{}'.format(num_all-num_bad), 'unqualified image:{}'.format(num_bad)]
sizes = [num_all-num_bad, num_bad]
colors = ['yellowgreen', 'lightskyblue']
plt.figure(figsize=(10, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

# 确保饼图是圆形的
plt.axis('equal')

# 显示图表
plt.show()

# for image in images_to_delete:
#     file_path = os.path.join(folder_path, image)
#     if os.path.exists(file_path):
#         os.remove(file_path)
#         print(f'Deleted: {image}')
#     else:
#         print(f'File not found, already deleted or never existed: {image}')

# for filename in images_to_delete:
#     # 替换扩展名为.png
#     new_filename = os.path.splitext(filename)[0] + '.png'
#     depth_to_delete.append(new_filename)
#
# for depth in depth_to_delete:
#     file_path = os.path.join(depth_folder, depth)
#     if os.path.exists(file_path):
#         os.remove(file_path)
#         print(f'Deleted: {depth}')
#     else:
#         print(f'File not found, already deleted or never existed: {depth}')
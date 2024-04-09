import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import laplace
from tqdm import tqdm
import cv2
import time

depth_path = "../LINEMOD/testdemo4/depth/"


# 创建掩码
def create_mask(depth):
    mask = np.ones(depth.shape, dtype=bool)
    rows, cols = depth.shape
    for x in range(rows):
        for y in range(cols):
            if depth[x][y] == 0:
                mask[x][y] = 0
    return mask


# 计算深度无效点
def count_badpoint(image):
    num_bad = 0
    for i in image.ravel():
        if i == 0:
            num_bad += 1
    return num_bad


# 创建一个均值滤波器
def mean_filter(image, point_position, filter_size):
    height, width = image.shape

    px = point_position[0]
    py = point_position[1]

    row_start = max(0, py - filter_size // 2)
    row_end = min(height, py + filter_size // 2 + 1)
    col_start = max(0, px - filter_size // 2)
    col_end = min(width, px + filter_size // 2 + 1)
    # 提取周围的像素值
    neighborhood = image[row_start:row_end, col_start:col_end]
    sum = 0
    num_light = 0
    for pixel in neighborhood.ravel():
        if pixel > 0:
            sum = sum + pixel
            num_light += 1
        else:
            continue
    # mean_value1 = np.mean(neighborhood)
    mean_value2 = sum / (num_light + 1e-5)
    # 判定有效修补
    image[px][py] = mean_value2

    return image


# 处理mask中的无效点
def mask_fix(depth_frame, mask_frame):
    depth_f = depth_frame.copy()
    # 遍历寻找无效点
    loss_points = []
    for x in range(depth_f.shape[0]):
        for y in range(depth_f.shape[0]):
            if mask_frame[x][y] == 0:
                loss_points.append((x, y))  # 获得所有无效点坐标
    # 遍历所有无效点坐标进行赋值
    j = 0
    loop = 0
    lastbad = 0
    while 1:
        loop += 1
        if j == len(loss_points) - 1:
            j = 0
        depth_f = mean_filter(depth_f, loss_points[j], 9)
        j = j + 1
        if loop % 1000 == 0:
            # print("bad point in result image = {}".format(count_badpoint(depth_f)))

            if count_badpoint(depth_f) == lastbad:
                break
            lastbad = count_badpoint(depth_f)
    return depth_f


import os
# 遍历文件夹中的所有文件
def traverse_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in tqdm(files):
            file_path = os.path.join(root, file)

            depth = Image.open(file_path)
            depth_array = np.array(depth)

            mask = create_mask(depth_array)
            result = mask_fix(depth_array, mask)
            # 保存修复后的图像
            result_path = file_path.replace("depth", "result")
            result_path = result_path.replace(".png", "_fix.png")

            Image.fromarray(result).save(result_path)
            # print("{} is done!".format(file_path))
# 示例：遍历当前文件夹下的所有文件

traverse_files(depth_path)

# print("---------------------------------")
# print("bad point in original image = {}".format(count_badpoint(depth_array)))
# print("bad point in result image = {}".format(count_badpoint(result)))

# # 显示修复前后的图像
# fig, axs = plt.subplots(1, 2, figsize=(10, 5))
# axs[0].imshow(depth_array, cmap='gray')
# axs[0].set_title('Original Image')
# axs[1].imshow(result, cmap='gray')
# axs[1].set_title('Repaired Image')
# plt.show()
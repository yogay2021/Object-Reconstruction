import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import laplace
from tqdm import tqdm
import cv2

depth_path = "../LINEMOD/testdemo4/depth/0.png"
depth = Image.open(depth_path)
depth_array = np.array(depth)
rows, cols = depth_array.shape

# 创建掩码
mask = np.ones(depth_array.shape, dtype=bool)
for x in range(rows):
    for y in range(cols):
        if depth_array[x][y] == 0:
            mask[x][y] = 0

# 计算深度无效点
def count_badpoint(image):
    num_bad = 0
    for i in image.ravel():
        if i == 0:
            num_bad += 1
    return num_bad

def tv_inpaint(image, mask, iterations=300, lambda_param=0.3, delta=0.5):

    # 合成需要修复的图像
    src_float = image.astype(np.float32)
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if mask[i, j] < 0:
                src_float[i, j] = 0.0
            if src_float[i, j] < 0:
                src_float[i, j] += 256.0

    # TV算法实现
    start_time = cv2.getTickCount()
    for _ in tqdm(range(iterations)):
        for i in range(1, image.shape[0] - 1):
            for j in range(1, image.shape[1] - 1):
                if mask[i, j] < 0:
                    UO, UN, UE, UW = src_float[i, j], src_float[i-1, j], src_float[i, j+1], src_float[i, j-1]
                    US, UE, USW, UNE = src_float[i+1, j], src_float[i, j+1], src_float[i-1, j+1], src_float[i-1, j-1]
                    USE = src_float[i+1, j-1]
                    U = np.array([UN, UE, UW, US, UNE, USW, USE])

                    Un, Ue, Uw, Us = np.sqrt((UO - U) ** 2 + delta ** 2)
                    W = 1.0 / (Un + Ue + Uw + Us + lambda_param + delta)
                    Wn, We, Ww, Ws = W[0], W[1], W[2], W[3]

                    Hon, Hoe, How, Hos = Wn / (Wn + We + Ww + Ws + lambda_param), \
                                       We / (Wn + We + Ww + Ws + lambda_param), \
                                       Ww / (Wn + We + Ww + Ws + lambda_param), \
                                       Ws / (Wn + We + Ww + Ws + lambda_param)

                    Hoo = lambda_param / (Wn + We + Ww + Ws + lambda_param)
                    src_float[i, j] = (Hon * UN + Hoe * UE + How * UW + Hos * US + Hoo * UO)

    end_time = cv2.getTickCount()
    elapsed_time = (end_time - start_time) / cv2.getTickFrequency()
    print("算法用时：{}秒".format(elapsed_time))

    return src_float

# 调用函数
result = tv_inpaint(depth_array, mask)



#

# 显示修复前后的图像
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].imshow(depth_array, cmap='gray')
axs[0].set_title('Original Image')
axs[1].imshow(result, cmap='gray')
axs[1].set_title('Repaired Image')
plt.show()


import os
import random

# 设置文件夹路径
folder_path = './LINEMOD/ob4/JPEGImages/'
root = './LINEMOD/ob4/'
# 读取文件夹中的所有文件
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# 计算test.txt和train.txt中应该包含的文件数量
test_size = int(len(files) * 0.2)
train_size = len(files) - test_size

# 随机打乱文件列表以确保随机分配
random.shuffle(files)

# 分配文件到test.txt和train.txt
test_files = files[:test_size]
train_files = files[test_size:]


# 写入test.txt
with open(root + 'test.txt', 'w') as f:
    for file in test_files:
        f.write(folder_path + file + '\n')

# 写入train.txt
with open(root + 'train.txt', 'w') as f:
    for file in train_files:
        f.write(folder_path + file + '\n')

print(f'{test_size} files have been written to test.txt.')
print(f'{train_size} files have been written to train.txt.')
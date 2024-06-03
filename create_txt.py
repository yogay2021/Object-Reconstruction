import os

# 设置要遍历的文件夹路径
folder_path = './LINEMOD/ob4/JPEGImages/'

# 设置要保存文件名的txt文件路径
output_file_path = './LINEMOD/ob4/valid.txt'

# 获取文件夹中所有文件和文件夹的名字
entries = os.listdir(folder_path)

# 打开一个文件用于写入
with open(output_file_path, 'w') as output_file:
    # 遍历所有条目
    for entry in entries:
        # 获取完整的文件路径
        full_path = os.path.join(folder_path, entry)
        # 检查这个路径是否是文件
        if os.path.isfile(full_path):
            # 写入文件名到txt文件，每行一个
            output_file.write(full_path + '\n')

print("文件名已保存到", output_file_path)
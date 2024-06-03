import os

folder_path = './LINEMOD/ob4/depth/'
new_path = './LINEMOD/ob4/depth_new/'
# 获取文件夹下的所有文件名
file_list = os.listdir(folder_path)

# 遍历文件列表进行重命名
for i, file_name in enumerate(file_list):
    # 获取文件扩展名
    file_ext = os.path.splitext(file_name)[1]
    # 构建新文件名
    new_file_name = '{}{}'.format(str(i), file_ext)
    # 拼接文件路径
    old_file_path = os.path.join(folder_path, file_name)
    new_file_path = os.path.join(new_path, new_file_name)
    # 重命名文件
    os.rename(old_file_path, new_file_path)
    print('{} --> {}'.format(old_file_path, new_file_path))

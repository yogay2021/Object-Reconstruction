# 0 中心 1 后右下 2 后右上 3 前右下 4 前右上 5 后左下 6 后左上 7 前左下 8 前左上
import os
import cv2
floder_path = "./LINEMOD/ob4/JPEGImages/"
save_path = "./LINEMOD/ob4/draw_gt/"
def draw_line(img_path, gt_floder_path, save_path):
    img = cv2.imread(img_path, 1)
    width = img.shape[1]
    height = img.shape[0]
    id = img_path.split('/')[-1]

    gt_points = list()
    with open(gt_floder_path, 'r') as file:
        for line in file:
            gt_xy = line.split(' ')
            for i in range(1, 18, 2):
                gt_x = width * float(gt_xy[i].strip())
                gt_y = height * float(gt_xy[i+1].strip())
                gt_points.append((int(gt_x), int(gt_y)))
    # 绘制点
    for point in gt_points:
        cv2.circle(img, point, 2, (255, 0, 255), 2)
    #y向连线
    cv2.line(img, gt_points[1], gt_points[2], (0, 0, 255), 1)
    cv2.line(img, gt_points[3], gt_points[4], (0, 0, 255), 1)
    cv2.line(img, gt_points[5], gt_points[6], (0, 0, 255), 1)
    cv2.line(img, gt_points[7], gt_points[8], (0, 0, 255), 1)
    #z向连线
    cv2.line(img, gt_points[1], gt_points[3], (0, 0, 255), 1)
    cv2.line(img, gt_points[2], gt_points[4], (0, 0, 255), 1)
    cv2.line(img, gt_points[5], gt_points[7], (0, 0, 255), 1)
    cv2.line(img, gt_points[6], gt_points[8], (0, 0, 255), 1)
    #x向连线
    cv2.line(img, gt_points[4], gt_points[8], (0, 0, 255), 1)
    cv2.line(img, gt_points[3], gt_points[7], (0, 0, 255), 1)
    cv2.line(img, gt_points[2], gt_points[6], (0, 0, 255), 1)
    cv2.line(img, gt_points[1], gt_points[5], (0, 0, 255), 1)

    cv2.imwrite(save_path + id, img)

def detec_inimg(gt_floder_path):
    gt_points = list()
    global num_bad
    with open(gt_floder_path, 'r') as file:
        for line in file:
            gt_xy = line.split(' ')
        for i in range(1, 21):
            if float(gt_xy[i]) < 0 or float(gt_xy[i]) > 1:
                num_bad += 1
                break

if __name__ == '__main__':
    out_img_list = []
    for root, dirs, files in os.walk(floder_path):
        for file in files:
            img_path = os.path.join(root, file)
            gt_floder_path = os.path.join(root.replace('JPEGImages', 'labels'), file[:-4] + '.txt')
            # draw_line(img_path, gt_floder_path, save_path)
            num_bad = 0
            detec_inimg(gt_floder_path)
            if num_bad != 0:
                out_img_list.append(gt_floder_path)
        print(len(out_img_list))

    for file_path in out_img_list:
        # 检查文件是否存在
        if os.path.isfile(file_path):
            # 删除文件
            os.remove(file_path)
            id = file_path.split('/')[-1]
            os.remove('./LINEMOD/ob4/JPEGImages/' + id.replace('txt', 'jpg'))
            print(f"文件 {file_path} 已被删除。")
            print(f"文件 {id.replace('txt', 'jpg')} 已被删除。")

import pyrealsense2 as rs
import numpy as np
import cv2
import cv2.aruco as aruco

# 配置摄像头与开启pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
profile = pipeline.start(config)
align_to = rs.stream.color
align = rs.align(align_to)

# 获取对齐的rgb和深度图
def get_aligned_images():
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()
    # 获取intelrealsense参数
    intr = color_frame.profile.as_video_stream_profile().intrinsics
    # 内参矩阵，转ndarray方便后续opencv直接使用
    intr_matrix = np.array([
        [intr.fx, 0, intr.ppx], [0, intr.fy, intr.ppy], [0, 0, 1]
    ])
    # 深度图-16位
    depth_image = np.asanyarray(aligned_depth_frame.get_data())
    # 深度图-8位
    depth_image_8bit = cv2.convertScaleAbs(depth_image, alpha=0.03)
    pos = np.where(depth_image_8bit == 0)
    depth_image_8bit[pos] = 255
    # rgb图
    color_image = np.asanyarray(color_frame.get_data())
    # return: rgb图，深度图，相机内参，相机畸变系数(intr.coeffs)
    return color_image, depth_image, intr_matrix, np.array(intr.coeffs)


if __name__ == "__main__":
    n = 0
    while 1:
        rgb, depth, intr_matrix, intr_coeffs = get_aligned_images()
        # 获取dictionary
        dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        # parameters = aruco.DetectorParameters()
        parameters = aruco.DetectorParameters_create()
        # 输入rgb图, aruco的dictionary, 相机内参, 相机的畸变参数
        # detector = aruco.ArucoDetector(dictionary, parameters)
        # corners, ids, rejected_img_points = detector.detectMarkers(rgb)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(rgb,
                                                              dictionary, parameters=parameters)

        # 估计出aruco码的位姿，0.045对应markerLength参数，单位是meter
        # rvec是旋转向量， tvec是平移向量
        rvec, tvec = aruco.estimatePoseSingleMarkers(corners, 0.06, intr_matrix, intr_coeffs)

        print("rvec = {}".format(rvec))
        print("tvec = {}".format(tvec))
        try:
        	# 在图片上标出aruco码的位置
            aruco.drawDetectedMarkers(rgb, corners)
            # 根据aruco码的位姿标注出对应的xyz轴, 0.05对应length参数，代表xyz轴画出来的长度
            aruco.drawAxis(rgb, intr_matrix, intr_coeffs, rvec, tvec, 0.05)
            cv2.imshow('RGB image', rgb)
        except:
            cv2.imshow('RGB image', rgb)
        key = cv2.waitKey(1)
        # 按键盘q退出程序
        if key & 0xFF == ord('q') or key == 27:
            pipeline.stop()
            break
        # 按键盘s保存图片
        elif key == ord('s'):
            n = n + 1
            # 保存rgb图
            cv2.imwrite('./img/rgb' + str(n) + '.jpg', rgb)

    cv2.destroyAllWindows()


RECORD_LENGTH = 100

import png
import pyrealsense2 as rs
import json
import logging

logging.basicConfig(level=logging.INFO)
import numpy as np
import cv2
import time
import os
import sys


# from config.DataAcquisitionParameters import DEPTH_THRESH

def make_directories(folder):
    if not os.path.exists(folder + "JPEGImages/"):
        os.makedirs(folder + "JPEGImages/")

def print_usage():
    print("Usage: record2.py <foldername>")
    print("foldername: path where the recorded data should be stored at")
    print("e.g., record2.py LINEMOD/mug")


if __name__ == "__main__":
    try:
        folder = sys.argv[1] + "/"
    except:
        print_usage()
        exit()

    FileName = 0
    make_directories(folder)

    pipeline = rs.pipeline()
    config = rs.config()
    # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start pipeline
    profile = pipeline.start(config)
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()

    # Color Intrinsics
    intr = color_frame.profile.as_video_stream_profile().intrinsics
    camera_parameters = {'fx': intr.fx, 'fy': intr.fy,
                         'ppx': intr.ppx, 'ppy': intr.ppy,
                         'height': intr.height, 'width': intr.width,
                         'depth_scale': profile.get_device().first_depth_sensor().get_depth_scale()
                         }

    with open(folder + 'intrinsics.json', 'w') as fp:
        json.dump(camera_parameters, fp)

    align_to = rs.stream.color
    align = rs.align(align_to)

    T_start = time.time()

    counter = 0
    while True:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        # aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not color_frame:
            continue

        # d = np.asanyarray(aligned_depth_frame.get_data())
        c = np.asanyarray(color_frame.get_data())

        # Visualize count down
        if cv2.waitKey(1) == ord('t'):
            # 保存 RGB 图像
            rgb_file_path = os.path.join(folder, 'JPEGImages', 'rgb_{:04d}.jpg'.format(counter))
            cv2.imwrite(rgb_file_path, c)
            print('color saved', rgb_file_path)
            counter += 1

        if time.time() - T_start > RECORD_LENGTH + 5:
            pipeline.stop()
            break

        if time.time() - T_start < 2:
            cv2.putText(c, str(5 - int(time.time() - T_start)), (240, 320), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 4,
                        (0, 0, 255), 2, cv2.LINE_AA)
        if time.time() - T_start > RECORD_LENGTH:
            cv2.putText(c, str(RECORD_LENGTH + 5 - int(time.time() - T_start)), (240, 320),
                        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 4, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow('COLOR IMAGE', c)

        # press q to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pipeline.stop()
            break

    # Release everything if job is finished
    cv2.destroyAllWindows()


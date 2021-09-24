import os
import shutil
import cv2
import numpy as np
from tqdm import tqdm


def convert_image_to_grey(image_path, dest_path='images') -> bool:
    """
    Function to convert color image to grey image
    :param image_path: path of image that you want to convert
    :param dest_path: path of destination directory where you want to save a new one
    :return: True if it's success
    """
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    image_name = os.path.basename(image_path)
    image_name = image_name.split('.')[0]

    img = cv2.imread(image_path)

    height, width, channel = img.shape
    grey_img = np.zeros((height, width, 1), dtype=np.uint8)

    for h in range(height):
        for w in range(width):
            grey_img[h, w] = 0.2989 * img[h, w, 2] + 0.5870 * img[h, w, 1] + 0.1140 * img[h, w, 0]

    path_to_image = os.path.join(dest_path, image_name + '_grey.png')
    cv2.imwrite(path_to_image, grey_img)
    return True


def convert_video_to_frames(video_path, frame_step=1, start=0, dest_path='images') -> bool:
    """
    Function to convert a video to the list of images that frame by frame
    :param video_path: path of video that you want to convert
    :param frame_step: distance between 2 frames
    :param start: the frame you want to start at
    :param dest_path: path of destination directory where you want to save the images
    :return:
    """
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    video_name = os.path.basename(video_path)
    video_name = video_name.split('.')[0]
    frame_directory = os.path.join(dest_path, video_name)

    if os.path.exists(frame_directory):
        shutil.rmtree(frame_directory)

    os.mkdir(frame_directory)

    cap = cv2.VideoCapture(video_path)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error")
        cap.release()
        return False

    # Read until video is completed
    cnt = start
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Total: ", total_frame)
    bar = tqdm(range(((total_frame - start) // frame_step) + 1),
               desc='{} converting: '.format(video_name),
               unit='frame')

    while True:
        ret, frame = cap.read()

        if ret:
            print("cnt: ", cnt)
            if cnt > total_frame:
                cap.release()
                return True

            cap.set(cv2.CAP_PROP_POS_FRAMES, cnt)
            path_to_image = os.path.join(frame_directory, 'frame' + str(cnt) + '.png')
            cv2.imwrite(path_to_image, frame)
            cnt += frame_step
            bar.update(1)
        else:
            cap.release()
            return True


from utilities.util import *
from utilities.drive_api import download_videos_google_drive


def main():
    videos_path = 'videos'
    images_path = 'images'

    str_01 = input("Do you have videos?(Y/n): ")

    if str_01 == 'Y' or str_01 == 'y':
        if download_videos_google_drive('Videos_Vip_Team', videos_path):
            print("Download Successful")
        else:
            print("Download error")
            return

    list_file = os.listdir(videos_path)
    print("FRAME CONVERTING!")
    for file in list_file:
        vid_path = os.path.join(videos_path, file)
        convert_video_to_frames(vid_path, 100, 0)
    print("Done!")

    print("GREY IMAGES CONVERTING!")
    list_img_direct = os.listdir(images_path)
    for direct in list_img_direct:
        print("direct: " + direct)
        list_img = os.listdir(os.path.join(images_path, direct))

        grey_image_directory = os.path.join(images_path, direct + '_grey')

        if os.path.exists(grey_image_directory):
            shutil.rmtree(grey_image_directory)

        os.mkdir(grey_image_directory)

        for images in list_img:
            img_path = os.path.join(images_path, direct, images)
            convert_image_to_grey(img_path, grey_image_directory)
    print("Done!")


if __name__ == '__main__':
    main()

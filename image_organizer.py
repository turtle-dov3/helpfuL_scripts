import exifread
import os
import shutil
import sys
from hachoir.metadata import *
from hachoir.parser import *

'''
quick and dirty approach to putting images and videos in specific folders based on when they were created.
'''


def process_files(path):
    photo_exts = ["jpg", "JPG", "JPEG", "jpeg", "PNG", "png"]
    video_exts = ["MOV", "mp4"]
    for file in os.listdir(path):
        array = file.rsplit(".", 1)
        if len(array) > 1:
            ext = array[1]
            if ext in photo_exts:
                print("processing file ", str(file))
                process_image(path, os.path.join(path, file))
            elif ext in video_exts:
                print("processing file ", str(file))
                process_video(path, os.path.join(path, file))


def create_new_folder(file, folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    try:
        shutil.move(file, folder_name)
    except IOError as e:
        print("error moving file",file,e)


def process_image(path, file):
    folder_name = None
    with open(file, 'rb') as image:
        tags = exifread.process_file(image)
        print(tags)
        if 'EXIF DateTimeOriginal' in tags:
            print(file, " has an original date time")
            folder_name = get_folder_name(tags['EXIF DateTimeOriginal'], path)
        else:
            print(file, " copying to unknown folder")
            folder_name = os.path.join(path, "unknown_date")
    create_new_folder(file, folder_name)


def get_folder_name(date_time, path):
    print(date_time)
    day = str(date_time).split(" ")[0]
    folder_name = os.path.join(path, day[:-3].replace(":", "-"))
    return folder_name


def process_video(path, vid_file):
    folder_name = None
    try:
        print("trying to get metadata from video ", vid_file)
        metaData = (extractMetadata(createParser(vid_file))).exportDictionary()
        print("metadata from video", metaData)
        creation_date = metaData["Metadata"]["Creation date"]
        print(creation_date)
        folder_name = get_folder_name(creation_date, path)
    except Exception as e:
        print("error getting metadata for file ", vid_file, e)
        folder_name = "unknown_date"
    create_new_folder(vid_file, folder_name)


if __name__ == '__main__':
    process_files(sys.argv[1])

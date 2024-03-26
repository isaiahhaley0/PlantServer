import time
import base64
import Services.DBHandler as DB
from PIL import Image, ImageSequence, ImageStat
import sys,os

mh = DB.DBHandler()


def get_photos(camera_name):
    photo_list = mh.get_photos(cam_name=camera_name)
    status = photo_list[0]["name"] +" selected"
    return photo_list

def resize_image(image):
    to_resize = Image.open(image)
    x,y = to_resize.size
    x = x * .5
    y = y * .5
    quality_val = 90
    image.save("filename", 'JPEG', quality=quality_val)


def make_gif(image_list, minutes_between_frames = 15):
    print("make gif")
    frames = [Image.open(image['save_path']) for image in image_list]
    frame_one = frames[0]
    save_location = "/mnt/share/Plant/gifs/"+image_list[0]['name']+time.time().__str__()+".gif"
    frame_one.save(save_location, append_images=frames[1::minutes_between_frames],
               save_all=True, duration=10, loop=0)
    print("gif done")
    return save_location


def get_photo_info(save_location):
    im = Image.open(save_location)
    stat = ImageStat.Stat(im)
    return stat.mean[0]


def get_photo(camera_name):
    photo_list = get_photos(camera_name)
    img = photo_list[-1]['save_path']
    return img

def get_photo_base64():
    return ""

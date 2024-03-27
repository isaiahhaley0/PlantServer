from PIL import Image
import tensorflow as tf
from datetime import datetime, timedelta
class Image_Bucket:
    def __init__(self, days_start, days_end, min_light, max_light):
        self.__start_datetime = datetime.now()-timedelta(hours=24*days_start)
        self.__end_datetime = datetime.now()-timedelta(hours=24*days_end)
        self.__photo_records =[]
        self.__min_light = min_light
        self.__max_light = max_light
        self.__light_range = max_light-min_light
        self.__light_threshold = (self.__light_range * 0.65)+min_light


    def try_add_photorecord(self, record):
        record_time = datetime.fromtimestamp(float(record['time']))
        if self.__start_datetime <= record_time < self.__end_datetime:
            self.__photo_records.append(record)
            print("Added Record")
            return True

        else:
            return False

    def get_hours_above_threshold(self):
        count_above_threshold = 0
        for p in self.__photo_records:
            if p["brightness"] >= self.__light_threshold:
                count_above_threshold+=1

        try:
            pct_above_thresh = count_above_threshold/len(self.__photo_records)
            return 24 * pct_above_thresh
        except:
            return 0

def get_image_info(image):
    image_info = {}

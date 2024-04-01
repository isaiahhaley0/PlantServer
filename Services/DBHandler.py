import datetime
import os
import time
import pymongo
import base64
from Services.image_analyzer import Image_Bucket
class DBHandler:
    def __init__(self):
        self.__started = False;
        self.__client = pymongo.MongoClient(
            os.environ['MONGODB_URI'])
        self.__db = self.__client.plantum
        print("running")

    def Insert_Reading(self, reading):
        self.__db = self.__client.plantum
        reading["time"] = time.time()
        coll = self.__db.environment_readings
        coll.insert_one(reading)

    def get_readings(self, trailing_minutes=1):
        coll = self.__db.environment_readings
        ms = trailing_minutes * 600

        query = {"time": {"$gt": time.time() - ms}}
        mine = list(coll.find(query))

        print(len(mine))
        return mine

    def get_last(self):
        coll = self.__db.environment_readings
        return coll.find_one({}, sort=[('_id', pymongo.DESCENDING)])

    def insert_photo_record(self, photo_record):
        coll = self.__db.photo_records
        coll.insert_one(photo_record)

    def get_camera_data(self):
        coll = self.__db.photo_records
        cameras = []
        records = coll.find({}).distinct('name')
        clist = {}
        clist['Cameras'] = records
        return clist

    def get_photos(self, cam_name):
        coll = self.__db.photo_records
        fltr = {"name": cam_name}
        print(cam_name)
        return list(coll.find(fltr))

    #def get_photos_last_days(self,start,end):

    def get_camera_info(self, name):
        plist = self.get_photos(name)
        cinfo = {}
        cinfo["Name"] = name
        cinfo["PhotoCount"] = len(plist)
        min = 1000000000000
        max = -1
        last = 0

        for p in plist:
            if "brightness" in p:
                if p["brightness"] > max:
                    max = p["brightness"]
                    tme = float(p["time"])
                    print(datetime.datetime.fromtimestamp(tme))

                elif p["brightness"] < min:
                    min = p["brightness"]
                    tme = float(p["time"])
                    print(datetime.datetime.fromtimestamp(tme))

                cinfo["Last_Brightness"] = p["brightness"]

        cinfo["Max_Brightness"] = max
        cinfo["Min_Brightness"] = min
        last_day = Image_Bucket(1,0,min,max)
        for p in plist:
            last_day.try_add_photorecord(p)

        print()
        cinfo["Hours_Of_Light"] = last_day.get_hours_above_threshold()
        return cinfo

    def Record_Watering(self, content):
        coll = self.__db.water_record
        coll.insert_one(content)

    def insert_plant(self, plant_json):
        coll = self.__db.plants
        coll.insert_one(plant_json)
        pass

    def get_plants(self):
        coll = self.__db.plants
        return coll.find({})

    def get_plant(self, name):
        coll = self.__db.plants
        return coll.find_one({"name":name})

    def insert_plant_photo_record(self, imageData):
        coll = self.__db.plant_image_record
        coll.insert_one(imageData)

    def get_plant_photo(self, name):

        coll = self.__db.plant_image_record
        return coll.find_one({"Plant":name}, sort=[('_id', pymongo.DESCENDING)])

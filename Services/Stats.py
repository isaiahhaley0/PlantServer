import time

import Services.DBHandler as DB


mh = DB.DBHandler()

class ReadingBucket:
    def __init__(self, time_start, time_end):
        self.__start = time_start
        self.__end = time_end
        self.__reading_list = []
        self.size = 0

    def try_add_reading(self,reading):
        if self.__end < reading["time"] < self.__start:
            self.__reading_list.append(reading)
            self.size += 1
            return True
        else:
            return False

    def get_as_dict(self):
        center_time = 0
        high = -1
        low = 100000
        sum = 0
        for read in self.__reading_list:
            center_time += read["time"]
            if read["light"] > high:
                high = read["light"]

            if read["light"] < low:
                low = read["light"]

            sum += read["light"]
        average = sum/len(self.__reading_list)
        hla = {}
        hla["high"] = high
        hla["low"] = low
        hla["average"] = average
        hla["time"] = center_time/len(self.__reading_list)
        return hla


def get_min_max():
    mx = -1
    mn = 1000000000000000000000
    rds = mh.get_readings(1440)
    for r in rds:
        if r["light"] > mx:
            mx = r["light"]

        if r["light"] < mn:
            mn = r["light"]

    return mn,mx


def get_hla(time_in_min = 3, num_buckets = 6):
    buckets = []
    nw = time.time()
    st = nw-(time_in_min * 600)
    bucket_size = (time_in_min * 600)/num_buckets
    for i in range(0,num_buckets):
        bucket = ReadingBucket( nw,nw-bucket_size)
        nw = nw - bucket_size
        buckets.append(bucket)

    rds = mh.get_readings(3)
    for rd in rds:
        for bucket in buckets:
            if bucket.try_add_reading(rd):
                break

    trt = []
    for buck in buckets:
        if buck.size > 0:
            trt.append(buck.get_as_dict())

    return trt











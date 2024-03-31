from Services.DBHandler import DBHandler


class PlantHandler:
    def __init__(self):
        self.dbh = DBHandler()

    def add_plant(self, plant_json):
        self.dbh.insert_plant(plant_json)
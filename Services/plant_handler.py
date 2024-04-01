from Services.DBHandler import DBHandler


class PlantHandler:
    def __init__(self):
        self.dbh = DBHandler()

    def add_plant(self, plant_json):
        self.dbh.insert_plant(plant_json)

    def get_all(self):
        plants = list(self.dbh.get_plants())
        for plant in plants:
            plant['_id'] = str(plant['_id'])
        return plants

    def get_plant(self, name):
        plant = self.dbh.get_plant(name)
        return plant

    def add_plant_image_record(self, imageData):
        self.dbh.insert_plant_photo_record(imageData)

    def get_plant_photo(self,plantName):
        return  self.dbh.get_plant_photo(plantName)
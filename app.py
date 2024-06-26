# This is a sample Python script.
import base64
import json
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

from flask import Flask, request, jsonify,Response,make_response, send_file
import Services.DBHandler as mh
import Services.Stats as st
import Services.CameraControl as CC
import Services.image_handler as ih
import Services.plant_handler as ph
from PIL import Image
import io
import os
import  platform
from flask_cors import CORS
app = Flask(__name__)
CORS(app)




mhd = mh.DBHandler()

@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/light", methods=['GET', 'PUT'])
def record_light_reading():
    rq = request
    data = request.json
    print(data["light"])
    mhd.Insert_Reading(data)
    return "heey"

@app.route("/camera",methods=['GET'])
def check_should_flash():
    flash = CC.should_flash()
    data = {
        "flash":flash,
    }
    print(flash)
    return jsonify(data)

@app.route("/camera_info",methods=['GET'])
def get_camera_information():
    name = request.args.get('Name')
    if name is not None:
        ci = mhd.get_camera_info(name)
        print(ci)
        return ci
    else:
        return mhd.get_camera_data()

@app.route("/photos",methods=['GET'])
def get_photos():
    name = request.args.get('name')
    print(name)
    photo_list = ih.get_photos(camera_name=name)
    print(len(photo_list))
    fp = ih.make_gif(photo_list)
    return send_file(fp)

@app.route("/photo",methods=['GET'])
def get_last_photo():
    name = request.args.get('name')
    print(name)
    if name is not None:
        photo = ih.get_photo(camera_name=name)
        return send_file(photo,mimetype='image/jpeg')


@app.route("/upload",methods=['POST'])
def upload_photo():
    print("uploading")
    image_raw_bytes = request.get_data()  # get the whole body
    tme = time.time().__str__()
    name = request.args.get('name')
    sequence = request.args.get('sequence')
    print(sequence)

    save_location = "/mnt/share/Plant/images/"+name+"_"+time.time().__str__()+".jpg"  # save to the same folder as the flask app live in
    info = {}
    info['time'] = tme
    info['save_path'] = save_location
    print(name)
    if name != "test":
        if name is None:
            name = 'cam1'

        info['name'] = name

        f = open(save_location, 'wb')  # wb for write byte data in the file instead of string
        f.write(image_raw_bytes)  # write the bytes from the request body to the file
        f.close()
        info['brightness']=ih.get_photo_info(save_location)
        mhd.insert_photo_record(info)

        print("Image saved")

        #return "image saved"
    data = {'message': 'Done', 'code': 'SUCCESS'}
    return make_response(jsonify(data),200)

#@app.route("/status")
#def get_server_status():

@app.route("/water",methods=['POST','PATCH'])
def water_plants():
    content = request.json
    print(content)
    mhd.Record_Watering(content)
    mhd.Update_Plant(content)
    res = {'status':'Watered'}
    return make_response(jsonify(res))

#update this 
@app.route("/plants",methods=['PUT','GET'])
def plant():
    planthandler = ph.PlantHandler()
    if request.method =='PUT':
        content = request.json
        if(platform.system() == "Windows"):
            newfolder = "Z:\\Plant\\Plants\\" + content["Name"]

            lnix = "/mnt/share/Plant/Plants/" + content["Name"]
            content["plant_photos"] = lnix
            planthandler.add_plant(content)
            if not os.path.exists(newfolder):
                os.makedirs(newfolder)
        else:
            newfolder = "/mnt/share/Plant/Plants/" + content["Name"]
            content["plant_photos"] = newfolder
            planthandler.add_plant(content)
            if not os.path.exists(newfolder):
                os.makedirs(newfolder)
        data = {'message': 'Done', 'code': 'SUCCESS'}
        return make_response(jsonify(data), 200)
    elif request.method =='GET':
        plants = planthandler.get_all()
        return json.dumps(plants)



@app.route("/plants/photos",methods=['PUT','GET'])
def plant_photo():
    planthandler = ph.PlantHandler()
    if request.method =='PUT':

        name = request.args.get('name')
        print(name)
        content = request.json
        print(content)
        if (platform.system() == "Windows"):
            newfolder = "Z:\\Plant\\Plants\\" + name +"\\"

            newf  = "/mnt/share/Plant/Plants/" + name
            with open(newfolder+content["Name"], "wb") as fh:
                fh.write(base64.b64decode(content['Base64Encoded']))
                imageData = {}
                imageData['Plant'] = name
                imageData['filepath'] = newf + "/" + content["Name"]
                imageData['upload_time'] = time.time()

                planthandler.add_plant_image_record(imageData)


        else:
            newfolder = "/mnt/share/Plant/Plants/" + name+"/"
            with open(newfolder+content["Name"], "wb") as fh:
                fh.write(base64.b64decode(content['Base64Encoded']))
        return 200
    elif request.method =='GET':
        name = request.args.get('name')
        photo = planthandler.get_plant_photo(name)
        if platform.system() == "Windows":
            fp = photo['filepath']
            fp = fp.replace("/mnt/share","Z:/")
            return send_file(fp, mimetype='image/jpeg')
        else:
            return send_file(photo['filepath'], mimetype='image/jpeg')



@app.route("/stats")
def get_stats():
    read = mhd.get_readings()

    avg = 0

    for r in read:
        avg = avg + r["light"]


    return st.get_hla()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


 

# Outlining the high level models for now, we need to discuss further in detail how we want to design our application 

from system_config import BaseStationConfigurations
from comms import get_input
import base64
#from exif import Image
import requests
import json
import logger
import datetime
import os

ML_API_url = 'http://127.0.0.1:8000/predict/'

#from exif import Image

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref =='W' :
        decimal_degrees = -decimal_degrees
    return decimal_degrees

#First, reset database and logs
files_to_reset = ['databases/predicitons.db',
                    'logs/prediciton_log.csv']
for file in files_to_reset:
    if os.path.exists(file):
        os.remove(file)
    # f = open(file, "x")

if __name__ == "__main__":
    # initialize the system configurations and store it
    config = BaseStationConfigurations()
    
    # gets list of image paths
    images = get_input()
    
    #### TESTING BLOCK START ####
    print("\n----------------------------------------")
    print("RUNNING TESTS ... ... ...")
    num_correct = 0
    #### TESTING BLOCK END ####
    
    for image_path in images:
        with open(image_path, "rb") as image_file:
            img_blob = base64.b64encode(image_file.read())
            encoded_img = img_blob.decode('utf-8')
            # print(encoded_string)
        
        # 2. Encode image into byte string (converted using blob)
        # 3. Request ML API for prediction
        response = requests.post(ML_API_url, data=json.dumps({"image": encoded_img}), headers = {"content-type": "application/json"})
        r = response.text
        #### TESTING BLOCK START ####
        expected_r = 'ERROR(BAD FILENAME)'
        try:
            if os.path.basename(image_path)[:2] == 'F_':
                expected_r = 'FIRE'
            elif os.path.basename(image_path)[:3] == 'NF_':
                expected_r = 'NO_FIRE'
        except Exception as e:
            print(e)
        print("\nTEST CASE: {}".format(image_path))
        print("Expected Result: {}".format(expected_r))
        print("Actual Result: {}".format(r))
        if expected_r == r:
            num_correct+=1
        #### TESTING CODE BLOCK END ####
        
        # return fields are TBD

        # img = Image(image_path)
        # if img.has_exif:
        #     try:
        #         img.gps_longitude
        #         coords = (decimal_coords(img.gps_latitude,
        #                 img.gps_latitude_ref),
        #                 decimal_coords(img.gps_longitude,
        #                 img.gps_longitude_ref))
        #         print({"imageTakenTime":img.datetime_original})
        #         print(coords)
        #     except AttributeError:
        #         print ('No Coordinates')
        # else:
        #     print('The Image has no EXIF information')
            
        # 4. Wait for prediction
        # 5. Send alert if fire, and log the (image, time, gps, prediction)
        currentDateTime = datetime.datetime.now()
        logger.add_prediction(config.log_id, currentDateTime, 12.5, -15.541, img_blob, r, config.db_name)
        config.log_id += 1
    
    #### TESTING BLOCK START ####
    print("\n ... ... ... TEST COMPLETE")
    print("{}/{} ({:.2f}%) predictions correct.".format(
        num_correct, len(images), 100*num_correct/len(images)
    ))
    print("----------------------------------------\n")
    #### TESTING BLOCK END ####
    
    logger.print_db_log(config.db_name)
    logger.close_databases(config.db_name)

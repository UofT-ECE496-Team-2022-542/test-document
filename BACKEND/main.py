# Outlining the high level models for now, we need to discuss further in detail how we want to design our application 

from system_config import BaseStationConfigurations
from drone import DroneController
from comms import get_input
import base64
#from exif import Image
import json
import logger
import datetime
import os

import cv2

##############################
### IMAGE CLASSIFIER SETUP ###
from image_classifier import ImageClassifier, forward_pass
import torch
from PIL import Image

global model
model = ImageClassifier()                         
model.load_state_dict(torch.load('ResNet_Models/epoch_'+str(4)+'.pth', map_location=torch.device('cpu')))
model.eval()


##############################


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref =='W' :
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def image_capture(drone):
    global count
    img = drone.drone.get_frame_read().frame
    #cv2.imshow("Image", img)
    cv2.waitKey(1)

    im_pil = Image.fromarray(img)
    r = forward_pass(model=model, image=im_pil)
    
    print("Model Result: {}".format(r))
    
    name = 'saved_images/image'+ r + str(count) + '.jpg'
    print(name)

    status = cv2.imwrite(name,img)
    count += 1
    print(status)
    
def surveillance(my_drone):
    rotate = 0
    offset1 = 1
    offset2 = 2
    while rotate < 8:
        image_capture(my_drone)
        if rotate % 2 == 0:  
            my_drone.drone.rotate_clockwise(45+offset1)
        else:
            my_drone.drone.rotate_clockwise(45+offset2)
        rotate += 1
    
def execute_flight_path(my_drone):
    image_capture(my_drone)
    my_drone.drone.takeoff()
    surveillance(my_drone)
    #go_xyz_speed(x, y, z, speed)
    my_drone.drone.go_xyz_speed(0,0,250,40)
    surveillance(my_drone)
    #up and right by 200 cm
    my_drone.drone.go_xyz_speed(200,200,0,40)
    surveillance(my_drone)
    my_drone.drone.go_xyz_speed(200,-200,0,40)
    my_drone.drone.go_xyz_speed(-200,-200,0,40)
    my_drone.drone.go_xyz_speed(-200,200,0,40)
    my_drone.drone.go_xyz_speed(0,0,-250,20)
    my_drone.drone.land()
    
def execute_flight_path(my_drone):
    while True:
        image_capture(my_drone)
   
    
#First, reset database and logs
files_to_reset = ['databases/predicitons.db',
                    'logs/prediciton_log.csv']
for file in files_to_reset:
    if os.path.exists(file):
        os.remove(file)
    # f = open(file, "x")

if __name__ == "__main__":
    count = 0
    # initialize the system configurations and store it
    config = BaseStationConfigurations()
    my_drone = DroneController()
    
    my_drone.drone.streamon()
    my_drone.pre_flight_checks()
    
    execute_flight_path(my_drone)
    
    my_drone.drone.streamoff()
    
        #### TESTING BLOCK START ####
    print("\n----------------------------------------")
    print("RUNNING TESTS ... ... ...")
    #### TESTING BLOCK END ####
    
    
    
    """ while True:
        with open(image_path, "rb") as image_file:
            img_blob = base64.b64encode(image_file.read())
            encoded_img = img_blob.decode('utf-8')
            # print(encoded_string)
        
        img = me.get_frame_read().frame
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        
        im_pil = Image.fromarray(img)
        r = forward_pass(model=model, image=im_pil)
        
        print("Actual Result: {}".format(r))
        
       
        currentDateTime = datetime.datetime.now()
        #logger.add_prediction(config.log_id, currentDateTime, 12.5, -15.541, img_blob, r, config.db_name)
        config.log_id += 1 """
    
   
    
    logger.print_db_log(config.db_name)
    logger.close_databases(config.db_name)

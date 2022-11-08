# Outlining the high level models for now, we need to discuss further in detail how we want to design our application 

from system_config import BaseStationConfigurations
from logging import log_input_data
from comms import get_input
import base64

# Since we only want to get a PoC out of this, we should focus mainly on the fundamental functions, 
# hence I think we should completely single-threaded-monolithic implementation

if __name__ == "__main__":
    
    # initialize the system configurations and store it
    # config = BaseStationConfigurations()  
    
    # gets list of image paths
    images = get_input()
    
    for image_path in images:
        
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        # print(encoded_string)
        
        # 2. Encode image into byte string (converted using blob)
        # 3. Request ML API for prediction
        # 4. Wait for prediction
        # 5. Send alert if fire, and log the (image, time, gps, prediction)
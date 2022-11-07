# Outlining the high level models for now, we need to discuss further in detail how we want to design our application 

from system_config import BaseStationConfigurations
from logging import log_input_data
from comms import get_input

# Since we only want to get a PoC out of this, we should focus mainly on the fundamental functions, 
# hence I think we should completely single-threaded-monolithic implementation

if __name__ == "__main__":
    
    # initialize the system configurations and store it
    #config = BaseStationConfigurations()  
    
    images = get_input()
    
    for image_path in images:
        
        print(image_path)
        
        # This waiting could be a huge bottleneck, we should consider creating 1 working thread but for now wait 
        # wait on next image
        
        
        
        # log the image into the database 
        
        # send image to ML API for analysis
        # wait for the ML API to finish
        
        # if it is true then send a signal to the user
        
        
    
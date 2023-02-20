from logger import initialize_database
from djitellopy import tello

class BaseStationConfigurations:
    db_name = "databases/predictions.db"
    log_id = 0
    
    def __init__(self) -> None:
                
        #initialize connection with database
        initialize_database(self.db_name)
        
 
        

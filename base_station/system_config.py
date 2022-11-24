from logger import initialize_database

class BaseStationConfigurations:
    db_name = "base_station/station_databases/prediction.db"
    log_id = 0
    
    
    def __init__(self) -> None:
        
        #initialize connection with drone
        #self.drone_conn = self.initialize_drone_connection()
        
        #initialize connection with database
        initialize_database(self.db_name)
        
    def initialize_drone_connection():
        NotImplemented
        
    
    

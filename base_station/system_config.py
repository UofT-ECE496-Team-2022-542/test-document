
class BaseStationConfigurations:
    def __init__(self) -> None:
        
        #initialize connection with drone
        self.drone_conn = self.initialize_drone_connection()
        
        #initialize connection with database
        self.database_conn = self.initialize_database()
        
    def initialize_drone_connection():
        NotImplemented
        
    
    

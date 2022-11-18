import sqlite3
import os

def get_connection(db_name):
    con = None
    try:
        con = sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
    cur = con.cursor()

    return (con, cur)

def initialize_database(con, cur):        
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS base_station
                    (timestamp TEXT PRIMARY KEY, lat REAL, lon REAL, image BLOB, prediction REAL)''')
        con.commit()
    except sqlite3.Error as e:
        print(e)
        
def close_databases(con, cur, db_name):
    cur.execute('''DROP TABLE IF EXISTS base_station''')
    con.commit()
    os.remove(db_name)
    
def add_prediction(timestamp, lat, lon, image, prediction):
       
    (con, cur) = get_connection_cursor(self.db_path)
    
    try:
        cur.execute("INSERT INTO base_station VALUES (?, ?, ?, ?, ?)",
                    (timestamp, lat, lon, image, prediction))
        con.commit()
    except:
        print("Was not able to insert into base_station database")
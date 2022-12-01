import sqlite3
import csv
import os

def get_connection(db_name):
    con = None
    try:
        con = sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
        
    cur = con.cursor()

    return (con, cur)

def initialize_database(db_path):        
    try:
        (con, cur) = get_connection(db_path)
    except Exception as e:
        print(e)
    
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS predictions
                    (id INT PRIMARY KEY NOT NULL,
                    timestamp TIMESTAMP, 
                    lat REAL, 
                    lon REAL, 
                    image BLOB, 
                    prediction REAL)''')
        con.commit()
        con.close()
    except sqlite3.Error as e:
        print(e)
        
def close_databases(db_path):
    (con, cur) = get_connection(db_path)
    cur.execute('''DROP TABLE IF EXISTS predictions''')
    con.commit()
    con.close()
    #os.remove(db_path)
    
def add_prediction(id, timestamp, lat, lon, image, prediction, db_path):
       
    (con, cur) = get_connection(db_path)
    
    try:
        cur.execute("INSERT INTO predictions VALUES (?, ?, ?, ?, ?, ?)",
                    (id, timestamp, lat, lon, image, prediction))
        con.commit()
        con.close()
    except sqlite3.Error as e:
        print(e)
        
def print_db_log(db_name):
    (con, cur) = get_connection(db_name)
    
    # open the file in the write mode
    f = open('logs/prediction_log.csv', 'w')

    # create the csv writer
    writer = csv.writer(f)
    
    for row in cur.execute('SELECT * FROM predictions'):
        writer.writerow(row)
    
    con.close()
    # close the file
    f.close()

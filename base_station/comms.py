import os

directory = 'base_station/input'

def get_input():
    
    file_paths = []
    
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            file_paths.append(f)
            #reading the input from the device
    
    return file_paths
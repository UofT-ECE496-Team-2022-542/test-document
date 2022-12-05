import requests
import json
import base64

URL = 'http://127.0.0.1:8000/predict/'

with open("input/F_0.jpg", "rb") as image_file:
    encoded_img = base64.b64encode(image_file.read()).decode("utf8")

r = requests.post(URL, data=json.dumps({"image": encoded_img}), headers = {"content-type": "application/json"})
print("Client test", r.text)
from flask import Flask, request
import base64
from PIL import Image
import io
import numpy as np

app = Flask(__name__)

@app.route('/predict/',methods=['POST'])
def predict():
    try:
        data = request.json
        img_b64 = data['image']
        img_bytes = base64.b64decode(img_b64.encode('utf-8'))
        img = Image.open(io.BytesIO(img_bytes))

        img_arr = np.asarray(img)
        return str(img_arr.shape)
    except Exception as e:
        print("ERROR: ", e)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
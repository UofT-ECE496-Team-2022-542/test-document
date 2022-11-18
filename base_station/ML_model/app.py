from flask import Flask, render_template, request, jsonify
from image_classifier import ImageClassifier, forward_pass
import torch
from PIL import Image
from io import BytesIO
import base64

global model
model = ImageClassifier()                         
model.load_state_dict(torch.load('ResNet_Models/epoch_'+str(4)+'.pth', map_location=torch.device('cpu')))

app = Flask(__name__)


@app.route('/')
def index_view():
    return render_template('index.html')

@app.route('/predict/',methods=['POST'])
def predict():
    try:
        data = request.json
        img_b64 = data['image']
        img_bytes = base64.b64decode(img_b64.encode('utf-8'))
        img = Image.open(BytesIO(img_bytes))
        response = forward_pass(model=model, image=img)
        print("RESPONSE: ", response)
        return response
    except Exception as e:
        print("ERROR: ", e)

if __name__ == '__main__':
    app.run(debug=True, port=8000)

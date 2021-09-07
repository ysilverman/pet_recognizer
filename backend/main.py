import time
from flask import Flask, request
import json
import pickle
import uuid
import io
from PIL import Image
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms


app = Flask(__name__)


def image_to_tensor(filedata):
    transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])
    
    img = Image.open(io.BytesIO(filedata.read()))
    image_tensor = transform(img)
    return image_tensor.unsqueeze(0)


def load_model():
    model = torch.load('full_model')
    model.eval()
    return model


def predict(filedata):
    image_tensor = image_to_tensor(filedata)
    output = model(image_tensor)
    probabilities = F.softmax(output, dim=1).data
    return class_names[probabilities.topk(1)[1].numpy()[0][0]]


classes = ["cat", "dog"]
class_names = {e: k for e,k in enumerate(classes)}
model = load_model()


@app.route('/predict', methods=["POST"])
def iris_post_handler():
    filedata = request.files["file"]
    result = predict(filedata)
    response = {
        "message": result,
    }
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0")

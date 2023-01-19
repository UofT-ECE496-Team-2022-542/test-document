import io
import os
import numpy as np

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torchvision.models
import torch.nn as nn
import torch.nn.functional as FF
from torchvision.models.resnet import ResNet, BasicBlock
from torch.autograd import Variable
from torchvision import datasets, transforms, models

from PIL import Image
from IPython.display import Image as photo, display

class ImageClassifier(ResNet):
    def __init__(self):
        super(ImageClassifier, self).__init__(BasicBlock, [2,2,2,2], num_classes=10)

        self.fc = nn.Sequential(
            nn.Linear(512 * BasicBlock.expansion, 64),
            nn.ReLU(),
            nn.Dropout(.2),
            nn.Linear(64, 2),
            nn.LogSoftmax(dim=1)
        )
        
def forward_pass(model, image, detailed_response=False):
    test_transforms = transforms.Compose([transforms.Resize(256), transforms.ToTensor(),])
    image_tensor = test_transforms(image).float()
    image_tensor = image_tensor.unsqueeze_(0)
    input = Variable(image_tensor)
    #input = input.to(device)
    output = model(input)
    
    if detailed_response:
        return str(1 + output.data[0][0]) + " FIRE, " + str(1 + output.data[0][1]) + " NO_FIRE"
    else:
        index = output.data.cpu().numpy().argmax()
        if index==0: return "FIRE"
        else: return "NO_FIRE"

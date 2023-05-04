import torch

import torch.nn as nn
from torchvision import models


def get_model(name="vgg16", pretrained=True):
    if name == "resnet18":
        model = models.resnet18(pretrained=pretrained)
    elif name == "resnet50":
        model = models.resnet50(pretrained=pretrained)
        # print('resnet50')
        # # Modify the last layer to match the number of classes in MNIST dataset
        # num_ftrs = model.fc.in_features
        # model.fc = torch.nn.Linear(num_ftrs, 10)

    elif name == "densenet121":
        model = models.densenet121(pretrained=pretrained)
    elif name == "alexnet":
        model = models.alexnet(pretrained=pretrained)
    elif name == "vgg16":
        model = models.vgg16(pretrained=pretrained)
        # Modify the input channels of the first convolutional layer
        model.features[0] = nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1)

    elif name == "vgg19":
        model = models.vgg19(pretrained=pretrained)
    elif name == "inception_v3":
        model = models.inception_v3(pretrained=pretrained)
    elif name == "googlenet":
        model = models.googlenet(pretrained=pretrained)

    if torch.cuda.is_available():
        return model.cuda()
    else:
        return model

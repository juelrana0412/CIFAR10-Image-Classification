import torch
import torch.nn as nn
from torchvision.models import swin_t

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available()
    else "cpu"
)



# CNN

def load_cnn(model_path):

    model = nn.Sequential(

        nn.Conv2d(3, 64, kernel_size=3, padding=1),
        nn.BatchNorm2d(64),
        nn.ReLU(inplace=True),

        nn.Conv2d(64, 64, kernel_size=3, padding=1),
        nn.BatchNorm2d(64),
        nn.ReLU(inplace=True),

        nn.MaxPool2d(2),
        nn.Dropout(0.25),


        # Block 2
        nn.Conv2d(64, 128, kernel_size=3, padding=1),
        nn.BatchNorm2d(128),
        nn.ReLU(inplace=True),

        nn.Conv2d(128, 128, kernel_size=3, padding=1),
        nn.BatchNorm2d(128),
        nn.ReLU(inplace=True),

        nn.MaxPool2d(2),
        nn.Dropout(0.30),

        # Block 3
        nn.Conv2d(128, 256, kernel_size=3, padding=1),
        nn.BatchNorm2d(256),
        nn.ReLU(inplace=True),

        nn.Conv2d(256, 256, kernel_size=3, padding=1),
        nn.BatchNorm2d(256),
        nn.ReLU(inplace=True),
        nn.MaxPool2d(2),
        nn.Dropout(0.35),

        # Block 4
        nn.Conv2d(256, 512, kernel_size=3, padding=1),
        nn.BatchNorm2d(512),
        nn.ReLU(inplace=True),

        nn.Conv2d(512, 512, kernel_size=3, padding=1),
        nn.BatchNorm2d(512),
        nn.ReLU(inplace=True),

        nn.MaxPool2d(2),
        nn.Dropout(0.40),


        nn.AdaptiveAvgPool2d((1, 1)),

        nn.Flatten(),
        nn.Linear(512, 512),
        nn.ReLU(inplace=True),
        nn.Dropout(0.5),

        nn.Linear(512, 256),
        nn.ReLU(inplace=True),
        nn.Dropout(0.4),

        nn.Linear(256, 10)
    )

    model.load_state_dict(
        torch.load(model_path, map_location=DEVICE)
    )

    model.eval()

    model.to(DEVICE)

    return model



# Swin-T

def load_swin(model_path):

    model = swin_t(weights=None)

    in_features = model.head.in_features

    model.head = nn.Sequential(
        nn.Linear(in_features,512),
        nn.BatchNorm1d(512),
        nn.GELU(),
        nn.Dropout(0.5),

        nn.Linear(512,256),
        nn.BatchNorm1d(256),
        nn.GELU(),
        nn.Dropout(0.3),

        nn.Linear(256,10)
    )

    model.load_state_dict(
        torch.load(model_path, map_location=DEVICE)
    )

    model.eval()

    model.to(DEVICE)

    return model
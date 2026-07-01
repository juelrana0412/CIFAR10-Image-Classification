import torch
from torchvision import transforms
from PIL import Image

from class_names import CLASSES
from model_loader import DEVICE


transform = transforms.Compose([

    transforms.Resize((224,224)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=(0.4914,0.4822,0.4465),
        std=(0.2023,0.1994,0.2010)
    )
])


def predict(image_path, model):

    image = Image.open(image_path).convert("RGB")

    image = transform(image)

    image = image.unsqueeze(0).to(DEVICE)

    with torch.no_grad():

        output = model(image)

        probabilities = torch.softmax(output, dim=1)

        confidence, predicted = torch.max(probabilities,1)

    return (
        CLASSES[predicted.item()],
        round(confidence.item()*100,2)
    )
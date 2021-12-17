import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# data_dir='/data4/pic/'
def classification_growth(data_path):
    model_dir='./app/func/model_growth2.pth'
    device='cpu'

    inputs = Image.open(data_path)

    data_transforms = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    inputs = data_transforms(inputs)
    class_names = ['1', '2', '3', '4']

    model = models.resnet50(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(class_names))
    model.eval()
    model.load_state_dict(torch.load(model_dir)) 
    with torch.no_grad():
      inputs = torch.unsqueeze(inputs,0)
      inputs = inputs.to(device)
      outputs = model(inputs)
      _, preds = torch.max(outputs, 1)
    
    return float(int(class_names[preds])/4)

def classification_health(data_path):
    model_dir='./app/func/model_health2.pth'
    device='cpu'
    
    inputs = Image.open(data_path)

    data_transforms = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    inputs = data_transforms(inputs)

    class_names = ['1', '2', '3']

    model = models.resnet50(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(class_names))
    model.eval()
    model.load_state_dict(torch.load(model_dir)) 

    with torch.no_grad():
       inputs = torch.unsqueeze(inputs,0)
       inputs = inputs.to(device)
       outputs = model(inputs)
       _, preds = torch.max(outputs, 1)
     
    return float(int(class_names[preds])/3)

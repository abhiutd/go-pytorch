# Standard imports
from concurrent import futures
import io
import requests
import numpy

from PIL import Image

import torch
from torchvision import models, transforms
from torch.autograd import Variable

def predict(*args, **kwargs):

	# download image using sent url
	response = requests.get(kwargs["image"])
	# create a pillow image
	image_pillow = Image.open(io.BytesIO(response.content))
	# preprocess image
	image_tensor = preprocess_image(image_pillow)
	image_tensor.unsqueeze_(0)

	# instantiate pre-trained squeezenet model
	squeeze = models.squeezenet1_1(pretrained=True)
	# select device for computation
	device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
	squeeze.to(device)
	
	image_variable = Variable(image_tensor)
	image_variable = image_variable.to(device)

	out = squeeze(image_variable)

	# download labels from url
	labels = {int(key):value for (key,value) in requests.get(kwargs["labels"]).json().items()}
	# get predicted class
	predict_label = labels[out.data.cpu().numpy().argmax()]

	return predict_label

def preprocess_image(image_pil):
    # define preprocessing transform
    normalize = transforms.Normalize(
       mean=[0.485, 0.456, 0.406],
       std=[0.229, 0.224, 0.225]
    )
    preprocess = transforms.Compose([
       transforms.Scale(256),
       transforms.CenterCrop(224),
       transforms.ToTensor(),
       normalize
    ])
    # apply preprocessing step to image
    image_tensor = preprocess(image_pil)
    return image_tensor

if __name__ == "__main__":
	kw = {
		"model" : "squeezenet", 
		"image" : "https://s3.amazonaws.com/outcome-blog/wp-content/uploads/2017/02/25192225/cat.jpg",
		"labels" : "https://s3.amazonaws.com/outcome-blog/imagenet/labels.json"
	     }
	arg = []
	prediction = predict(*arg, **kw)
	print("prediction: " + prediction)	

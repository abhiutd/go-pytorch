# Copyright 2018 MLModelScope authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC pytorch server."""

# Standard imports
from concurrent import futures
import time
import sys
import numpy
import io
import requests

# Pillow import
from PIL import Image

# PyTorch specific imports
import torch
from torchvision import models, transforms
from torch.autograd import Variable

# gRPC specific imports
import grpc
import dlframework_pb2
import dlframework_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

# select device for computation
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# label url for matching with predicted class
label_url = 'https://s3.amazonaws.com/outcome-blog/imagenet/labels.json'

class Dlframework(dlframework_pb2_grpc.DlframeworkServicer):

    def Predict(self, request, context):
        # download image using sent image_url
        response = requests.get(request.image)
        # create a pillow image
        img_pil = Image.open(io.BytesIO(response.content)) 
        # preprocess image
        img_tensor = preprocess_image(img_pil)
        img_tensor.unsqueeze_(0)

        # instantiate pre-trained squeezenet model
        squeeze = models.squeezenet1_1(pretrained=True)
        squeeze.to(device)

        img_variable = Variable(img_tensor)
        # transfer image to GPU
        img_variable = img_variable.to(device)

        with torch.autograd.profiler.profile() as prof:
            # forward pass
            for iterations in range(30):
                fc_out = squeeze(img_variable)

        # download labels to make output human-readable
        labels = {int(key):value for (key, value)
          in requests.get(label_url).json().items()}
        # get predicted class
        predict_label = labels[fc_out.data.cpu().numpy().argmax()]
        print(prof.table())

        return dlframework_pb2.DlReply(prediction=predict_label)

def serve():
    print('Ready to serve...')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dlframework_pb2_grpc.add_DlframeworkServicer_to_server(Dlframework(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

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

if __name__ == '__main__':

    # start serving
    serve()
    

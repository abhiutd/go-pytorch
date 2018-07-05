# Copyright 2015 gRPC authors.
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
"""The Python implementation of the GRPC dlframework server."""

from concurrent import futures
import time
import sys
import numpy

import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.transforms as transforms

import grpc

import dlframework_pb2
import dlframework_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

# TODO:classes for CIFAR10
classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# select device for computation
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class Dlframework(dlframework_pb2_grpc.DlframeworkServicer):

    def Predict(self, request, context):
        
        # fetches prediction for one indexed image
        # fetch image for inference
        dataiter = iter(testloader)
        images, labels = dataiter.next()
        # inference to be done on GPU
        images, labels = images.to(device), labels.to(device)
        outputs = net(images)
        _, predicted = torch.max(outputs, 1)
        print('Predicted: ', ' '.join('%5s' % classes[predicted[j]]
                              for j in range(4)))
        return dlframework_pb2.DlReply(prediction=classes[predicted[1]])

# define CNN
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

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

def fetch_dataset():
    transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    global trainset, trainloader
    global testset, testloader
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=2)

    testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=4,
                                         shuffle=False, num_workers=2)

def load_model():
    global model
    model = torchvision.models.resnet50(pretrained=True)
    model.eval()
    model.cuda()

def create_model():
    
    print("Instantiate model...")
    global net
    net = Net()
    net.to(device)

    print("Define training parameters...")
    # define loss function and optimiser
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    print("Start training...")
    # train network
    for epoch in range(2):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs
            inputs, labels = data
            # send it to GPU
            inputs, labels = inputs.to(device), labels.to(device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:    # print every 2000 mini-batches
                #print('[%d, %5d] loss: %.3f' %
                #  (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0

    print('Finished training...')


if __name__ == '__main__':
    
    # fetch dataset before serving requests
    fetch_dataset()

    # create a (trained) model
    create_model()
     
    # start serving
    serve()

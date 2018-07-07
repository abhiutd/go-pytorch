'''
	Another application using Super-resolution
	pre-trained pytorch model for inference
'''
import onnx
from torch import nn
import torch.utils.model_zoo as model_zoo
import torch.onnx
import torch.nn as nn
import torch.nn.init as init

# Load the ONNX ModelProto object. model is a standard Python protobuf object
model = onnx.load("./model/super_resolution.onnx")

# Input to the model
batch_size = 1
x = torch.randn(batch_size, 1, 224, 224, requires_grad=True)

# Run inference
model.forward(x)

print('Imported ONNX in PyTorch successfully!!!')

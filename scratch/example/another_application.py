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
import torch

### If you comment it out, you would get
### Attribute error
### We need access to .pth + its source code
### for class definitions and dependent packages
### Reference: https://discuss.pytorch.org/t/loading-pytorch-model-without-a-code/12469
# import original class
from application import SuperResolutionNet

# import pytorch specific model file
model = torch.load("./model/super_resolution.pth")

# run inference on loaded model

### Import ONNX model into PyTorch is not currently supported
# Load the ONNX ModelProto object. model is a standard Python protobuf object
#model = onnx.load("./model/super_resolution.onnx")

# Input to the model
batch_size = 1
x = torch.randn(batch_size, 1, 224, 224, requires_grad=True)

# Run inference
model.forward(x)

print('Imported PTH in PyTorch successfully!!!')

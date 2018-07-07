As of July 2018, PyTorch supports exporting models (and their trained weights) in ONNX format. PyTorch-devs suggest using Caffe2 to deploy trained PyTorch models as their focus is not on developing a model serving backend for PyTorch. Hence, they do not support importing ONNX format models.

`application.py` -> exports model to .onnx
`another_application.py` -> tries to run loaded .onnx model in PyTorch, but is unsuccessful  

from dummy_model import ReallySimpleModel
import torch

# print model
net = ReallySimpleModel()
print(net)

# save model
torch.save(net, "./net.checkpoint.pth.tar")



import torch
import torchvision

# An instance of your model.
model = torchvision.models.alexnet()

# An example input you would normally provide to your model's forward() method.
example = torch.rand(1, 3, 224, 224)

# Use torch.jit.trace to generate a torch.jit.ScriptModule via tracing.
traced_script_module = torch.jit.trace(model, example, check_trace=False)

# generate model file
traced_script_module.save("./work/example/alexnet/alexnet.pt")

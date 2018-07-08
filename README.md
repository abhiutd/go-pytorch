# go-pytorch
We intend to interface PyTorch with our go code, which would enable us to call the framework as well as profile it. The scratch folder contains two ways we can follow - embedding CPython interpreter (via a publicly available lightweight Go wrapper around it ) and gRPC.

gRPC is the preferred methodlogy based on our literature survey. Here, we would be running a server which would contain PyTorch based service, and every call would essentially be a Go client calling our server. We choose this as it keeps both of them modular.

Go client is supposed to perform the following functions :
(1) Fetch image(s)
(2) Preprocess it (which includes converting it to byte code)
(3) Call `predict()` function with image and model link on the PyTorch server

PyTorch server is supposed to perform the following functions :
(4) Fetch model (in .pth format) from the web or filesystem
(5) Start running go-cupti (as a shared library)
(6) Turn on layer-by-layer profiling in PyTorch
(7) Run `predict()` on sent image
(8) Send back predicted output
(9) Output CUPTI and PyTorch traces  

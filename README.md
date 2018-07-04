# go-pytorch
We intend to interface PyTorch with our go code, which would enable us to call the framework as well as profile it. The scratch folder contains two ways we can follow - embedding CPython interpreter (via a publicly available lightweight Go wrapper around it ) and gRPC.

gRPC is the preferred methodlogy based on our literature survey. Here, we would be running a server which would contain PyTorch based service, and every call would essentially be a Go client calling our server. We choose this as it keeps both of them modular.

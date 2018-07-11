package main

import python "github.com/sbinet/go-python"

func main(){

	python.Initialize()
	defer python.Finalize()

	greetModule := python.PyImport_ImportModule("hello_world")
	if greetModule == nil{
		panic("Error importing module")
	}

	greetFunc := greetModule.GetAttrString("hello")
	if greetFunc == nil{
		panic("Error importing function")
	}

	greetFunc.Call(python.PyTuple_New(0), python.PyDict_New())
}

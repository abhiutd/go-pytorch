package main

import (
        "fmt"
        "log"

        "github.com/sbinet/go-python"
)

func init() {
        err := python.Initialize()
        if err != nil {
                panic(err.Error())
        }
}

func main() {

        fmt.Printf("Performing inference using PyTorch...\n")
        m := python.PyImport_ImportModule("helper")
        if m == nil {
		fmt.Printf("Error : %s", python.PyString_AsString(python.PyErr_Print()))
                log.Fatalf("Could not import 'helper'\n")
	}

        predictor := m.GetAttrString("predict")
        if predictor == nil {
                log.Fatalf("Could not import predict()\n")
        }

        // keyword arguments
        kw := python.PyDict_New()
        err_1 := python.PyDict_SetItem(
                kw,
                python.PyString_FromString("model"),
                python.PyString_FromString("squeezenet"),
        )
        if err_1 != nil {
                log.Fatalf("error_1: %v\n", err_1)
        }

        err_2 := python.PyDict_SetItem(
                kw,
                python.PyString_FromString("image"),
                python.PyString_FromString("https://s3.amazonaws.com/outcome-blog/wp-content/uploads/2017/02/25192225/cat.jpg"),
        )
        if err_2 != nil {
                log.Fatalf("error_2: %v\n", err_2)
        }

	err_3 := python.PyDict_SetItem(
                kw,
                python.PyString_FromString("label"),
                python.PyString_FromString("https://s3.amazonaws.com/outcome-blog/imagenet/labels.json"),
        )
        if err_3 != nil {
                log.Fatalf("error_3: %v\n", err_1)
        }

	args := python.PyTuple_New(0)
	prediction := predictor.Call(args, kw)
	if prediction == nil {
		log.Fatalf("error calling predict()\n")
	}

	fmt.Printf("prediction : %s", python.PyString_AsString(prediction))

}

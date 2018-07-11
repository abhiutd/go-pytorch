// main.go
// try out embedding python function in Go application
package main

/*
// go preamble
#include <stdlib.h>
*/
import "C"
import (
	"fmt"
	"github.com/sbinet/go-python"
)

func main() {

	// initialise cpython interpreter  
	python.Initialize()
	defer python.Finalize()

	// import module 
	sumModule := python.PyImport_ImportModule("helper")
	if sumModule == nil {
		panic("Error importing module")
	}

	// import function
	sumFunc := sumModule.GetAttrString("sum_helper")
	if sumFunc == nil {
                panic("Error importing function")
        }

	// TODO create a list of numbers to be added
	//plist := python.PyList_New(2)
	//python.PyList_Append(plist, python.PyLong_FromLong(1))
	//fmt.Printf("%b\n", python.PyType_Check(plist))
	fmt.Printf("Print\n")
	// TODO pass list to python function 
	// call python function
	// WORKS when sending empty list
	// Note: mandatory to send *args and **kwargs
	// lets try it out for strings
	gostr := "WORKS!"
	pystr := python.PyString_FromString(gostr)

	sumFunc.Call(pystr, python.PyDict_New())

}


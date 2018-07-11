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

	fmt.Printf("Adding two numbers...\n")
	m := python.PyImport_ImportModule("helper")
	if m == nil {
		log.Fatalf("Could not import 'helper'\n")
	}

	add := m.GetAttrString("add_numbers")
	if add == nil {
		log.Fatalf("Could not import add_numbers()\n")
	}

	// keyword arguments
	nums := python.PyDict_New()
	err_1 := python.PyDict_SetItem(
		nums,
		python.PyString_FromString("a"),
		python.PyInt_FromLong(3),
	)
	if err_1 != nil {
		log.Fatalf("error_1: %v\n", err_1)
	}

	err_2 := python.PyDict_SetItem(
                nums,
                python.PyString_FromString("b"),
                python.PyInt_FromLong(7),
        )
        if err_2 != nil {
                log.Fatalf("error_2: %v\n", err_2)
        }

	args := python.PyTuple_New(0)
	out := add.Call(args, nums)
	if out == nil {
		log.Fatalf("error calling add()\n")
	}

	ans := python.PyString_AsString(out)
	fmt.Printf("%d\n", ans)

}

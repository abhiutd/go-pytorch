package main

import python "github.com/sbinet/go-python"

func main() {

	python.Initialize()
	python.PyRun_SimpleString("print 'hello, world!'")
	python.Finalize()

}

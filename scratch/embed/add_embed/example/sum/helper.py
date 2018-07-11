from __future__ import print_function

def add_numbers(*args, **kwargs):
	acc = 0
	for key, value in kwargs.items():
		acc += value
	return str(acc)

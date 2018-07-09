'''
	Dummy network class definition
	not dependent on any package
	Expected : saving and loading should
	work fine without source code access

'''

import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np


class ReallySimpleModel():
    def forward(self, x):
        x = np.zeros(5)



# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC operation.Operation server."""

from concurrent import futures
import time
import sys
import numpy

import pycuda.driver as cuda
#import pycuda.autoinit
from pycuda.tools import make_default_context
from pycuda.compiler import SourceModule

import grpc

import operation_pb2
import operation_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Operation(operation_pb2_grpc.OperationServicer):

    def Add(self, request, context):
        # call add on cpu and gpu
        sum_1 = Add_cpu(request.a, request.b)
        # does not add those numbers on gpu
        # but mimics gpu action by actually doublifying
        # a randomly generated 2-D array
        sum_2 = Add_gpu(request.a, request.b) 
        # assert both values
        assert 2*sum_1 == sum_2
        # explicit addition
        #sum_1 = request.a + request.b
        return operation_pb2.OpReply(c=sum_2)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    operation_pb2_grpc.add_OperationServicer_to_server(Operation(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

def Add_cpu(x, y):
    return x+y

def Add_gpu(x, y):
    cuda.init()
    ctx = make_default_context()
    device = ctx.get_device()

    a = numpy.random.randn(4,4)
    a = a.astype(numpy.float32)
    a_gpu = cuda.mem_alloc(a.nbytes)
    cuda.memcpy_htod(a_gpu, a)

    '''
    x_gpu = cuda.mem_alloc(sys.getsizeof(x))
    y_gpu = cuda.mem_alloc(sys.getsizeof(y))
    z_gpu = cuda.mem_alloc(sys.getsizeof(x))
    cuda.memcpy_htod(x_gpu, x)
    cuda.memcpy_htod(y_gpu, y)
    
    mod = SourceModule("""
      __global__ void add(int *x_addr, int *y_addr, int* z_addr)
      {
          // naive computation
          sum = *x_addr + *y_addr;
          *z_addr = sum;
      }
    """)

    func = mod.get_function("add")
    func(x_gpu, y_gpu, z_gpu, block=(4,4,1))
    '''

    mod = SourceModule("""
      __global__ void doublify(float *a)
      {
          int idx = threadIdx.x + threadIdx.y*4;
          a[idx] *= 2;
      }
    """)
    func = mod.get_function("doublify")
    func(a_gpu, block=(4,4,1))
    
    #cuda.memcpy_dtoh(x, z_gpu)
    a_doubled = numpy.empty_like(a)
    cuda.memcpy_dtoh(a_doubled, a_gpu)
    
    ctx.pop()
    
    return 2*(x+y)

if __name__ == '__main__':
    serve() 

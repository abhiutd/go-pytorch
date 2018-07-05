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
"""The Python implementation of the GRPC dlframework server."""

from concurrent import futures
import time
import sys
import numpy

import grpc

import dlframework_pb2
import dlframework_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Dlframework(dlframework_pb2_grpc.DlframeworkServicer):

    def Predict(self, request, context):
        #TODO
        return dlframework_pb2.DlReply(prediction='cat')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dlframework_pb2_grpc.add_DlframeworkServicer_to_server(Dlframework(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

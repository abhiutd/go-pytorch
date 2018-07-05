# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: operation.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='operation.proto',
  package='operation',
  syntax='proto3',
  serialized_pb=_b('\n\x0foperation.proto\x12\toperation\"!\n\tOpRequest\x12\t\n\x01\x61\x18\x01 \x01(\x05\x12\t\n\x01\x62\x18\x02 \x01(\x05\"\x14\n\x07OpReply\x12\t\n\x01\x63\x18\x01 \x01(\x05\x32>\n\tOperation\x12\x31\n\x03\x41\x64\x64\x12\x14.operation.OpRequest\x1a\x12.operation.OpReply\"\x00\x42,\n\x1aio.grpc.examples.operationB\x07OpProtoP\x01\xa2\x02\x02OPb\x06proto3')
)




_OPREQUEST = _descriptor.Descriptor(
  name='OpRequest',
  full_name='operation.OpRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='operation.OpRequest.a', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='b', full_name='operation.OpRequest.b', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=63,
)


_OPREPLY = _descriptor.Descriptor(
  name='OpReply',
  full_name='operation.OpReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='c', full_name='operation.OpReply.c', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=65,
  serialized_end=85,
)

DESCRIPTOR.message_types_by_name['OpRequest'] = _OPREQUEST
DESCRIPTOR.message_types_by_name['OpReply'] = _OPREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OpRequest = _reflection.GeneratedProtocolMessageType('OpRequest', (_message.Message,), dict(
  DESCRIPTOR = _OPREQUEST,
  __module__ = 'operation_pb2'
  # @@protoc_insertion_point(class_scope:operation.OpRequest)
  ))
_sym_db.RegisterMessage(OpRequest)

OpReply = _reflection.GeneratedProtocolMessageType('OpReply', (_message.Message,), dict(
  DESCRIPTOR = _OPREPLY,
  __module__ = 'operation_pb2'
  # @@protoc_insertion_point(class_scope:operation.OpReply)
  ))
_sym_db.RegisterMessage(OpReply)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\032io.grpc.examples.operationB\007OpProtoP\001\242\002\002OP'))

_OPERATION = _descriptor.ServiceDescriptor(
  name='Operation',
  full_name='operation.Operation',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=87,
  serialized_end=149,
  methods=[
  _descriptor.MethodDescriptor(
    name='Add',
    full_name='operation.Operation.Add',
    index=0,
    containing_service=None,
    input_type=_OPREQUEST,
    output_type=_OPREPLY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_OPERATION)

DESCRIPTOR.services_by_name['Operation'] = _OPERATION

# @@protoc_insertion_point(module_scope)
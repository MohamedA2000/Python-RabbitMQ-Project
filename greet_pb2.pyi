from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DelayedReply(_message.Message):
    __slots__ = ["message", "request"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    message: str
    request: _containers.RepeatedCompositeFieldContainer[HelloRequest]
    def __init__(self, message: _Optional[str] = ..., request: _Optional[_Iterable[_Union[HelloRequest, _Mapping]]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class HelloReply(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class HelloRequest(_message.Message):
    __slots__ = ["greeting", "name"]
    GREETING_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    greeting: str
    name: str
    def __init__(self, name: _Optional[str] = ..., greeting: _Optional[str] = ...) -> None: ...

class MineDisarmed(_message.Message):
    __slots__ = ["pin", "serialNumber"]
    PIN_FIELD_NUMBER: _ClassVar[int]
    SERIALNUMBER_FIELD_NUMBER: _ClassVar[int]
    pin: int
    serialNumber: str
    def __init__(self, serialNumber: _Optional[str] = ..., pin: _Optional[int] = ...) -> None: ...

class MineNumber(_message.Message):
    __slots__ = ["i", "j"]
    I_FIELD_NUMBER: _ClassVar[int]
    J_FIELD_NUMBER: _ClassVar[int]
    i: int
    j: int
    def __init__(self, i: _Optional[int] = ..., j: _Optional[int] = ...) -> None: ...

class MineSerialNumber(_message.Message):
    __slots__ = ["serialNumber"]
    SERIALNUMBER_FIELD_NUMBER: _ClassVar[int]
    serialNumber: str
    def __init__(self, serialNumber: _Optional[str] = ...) -> None: ...

class Pin(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class RoverCommands(_message.Message):
    __slots__ = ["commands", "hasCommands"]
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    HASCOMMANDS_FIELD_NUMBER: _ClassVar[int]
    commands: str
    hasCommands: bool
    def __init__(self, hasCommands: bool = ..., commands: _Optional[str] = ...) -> None: ...

class RoverMap(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: str
    def __init__(self, data: _Optional[str] = ...) -> None: ...

class RoverNumber(_message.Message):
    __slots__ = ["num"]
    NUM_FIELD_NUMBER: _ClassVar[int]
    num: int
    def __init__(self, num: _Optional[int] = ...) -> None: ...

class RoverStatus(_message.Message):
    __slots__ = ["hasExploded", "num"]
    HASEXPLODED_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    hasExploded: bool
    num: int
    def __init__(self, num: _Optional[int] = ..., hasExploded: bool = ...) -> None: ...

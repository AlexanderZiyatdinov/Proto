from typing import NewType

string = NewType('string', str)
double = NewType('double', float)
fixed32 = NewType('fixed32', int)
fixed64 = NewType('fixed64', int)
sfixed32 = NewType('sfixed32', int)
sfixed64 = NewType('sfixed64', int)
sint32 = NewType('sint32', int)
sint64 = NewType('sint64', int)
uint = NewType('uint', int)  # is not a part of the standard
uint32 = NewType('uint32', int)
uint64 = NewType('uint64', int)
int32 = uint32
int64 = uint64
NoneType = type(None)

# automatically generated, do not modify

# namespace: connectiongroup

import flatbuffers

class IntBBox(object):
    __slots__ = ['_tab']

    # IntBBox
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # IntBBox
    def Coordinates(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # IntBBox
    def CoordinatesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def IntBBoxStart(builder): builder.StartObject(1)
def IntBBoxAddCoordinates(builder, coordinates): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(coordinates), 0)
def IntBBoxStartCoordinatesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def IntBBoxEnd(builder): return builder.EndObject()

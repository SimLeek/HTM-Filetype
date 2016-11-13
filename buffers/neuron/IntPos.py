# automatically generated, do not modify

# namespace: neuron

import flatbuffers

class IntPos(object):
    __slots__ = ['_tab']

    # IntPos
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # IntPos
    def Coordinates(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Float32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # IntPos
    def CoordinatesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def IntPosStart(builder): builder.StartObject(1)
def IntPosAddCoordinates(builder, coordinates): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(coordinates), 0)
def IntPosStartCoordinatesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def IntPosEnd(builder): return builder.EndObject()

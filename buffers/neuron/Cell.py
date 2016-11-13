# automatically generated, do not modify

# namespace: neuron

import flatbuffers

class Cell(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsCell(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Cell()
        x.Init(buf, n + offset)
        return x


    # Cell
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Cell
    def PositionType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # Cell
    def Position(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            from flatbuffers.table import Table
            obj = Table(bytearray(), 0)
            self._tab.Union(obj, o)
            return obj
        return None

    # Cell
    def LastUsedIteration(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

    # Cell
    def UID(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Cell
    def ConnectionsUID(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Cell
    def Segments(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .Segment import Segment
            obj = Segment()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Cell
    def SegmentsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def CellStart(builder): builder.StartObject(6)
def CellAddPositionType(builder, positionType): builder.PrependUint8Slot(0, positionType, 0)
def CellAddPosition(builder, position): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(position), 0)
def CellAddLastUsedIteration(builder, lastUsedIteration): builder.PrependUint32Slot(2, lastUsedIteration, 0)
def CellAddUID(builder, UID): builder.PrependUint64Slot(3, UID, 0)
def CellAddConnectionsUID(builder, connectionsUID): builder.PrependUint64Slot(4, connectionsUID, 0)
def CellAddSegments(builder, segments): builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(segments), 0)
def CellStartSegmentsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def CellEnd(builder): return builder.EndObject()

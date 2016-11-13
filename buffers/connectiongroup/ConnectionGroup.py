# automatically generated, do not modify

# namespace: connectiongroup

import flatbuffers

class ConnectionGroup(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsConnectionGroup(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = ConnectionGroup()
        x.Init(buf, n + offset)
        return x


    # ConnectionGroup
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # ConnectionGroup
    def UID(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # ConnectionGroup
    def NumCells(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

    # ConnectionGroup
    def MaxSegmentsPerCell(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 255

    # ConnectionGroup
    def MaxSynapsesPerSegment(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 255

    # ConnectionGroup
    def BboxType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # ConnectionGroup
    def Bbox(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            from flatbuffers.table import Table
            obj = Table(bytearray(), 0)
            self._tab.Union(obj, o)
            return obj
        return None

def ConnectionGroupStart(builder): builder.StartObject(6)
def ConnectionGroupAddUID(builder, UID): builder.PrependUint64Slot(0, UID, 0)
def ConnectionGroupAddNumCells(builder, numCells): builder.PrependUint32Slot(1, numCells, 0)
def ConnectionGroupAddMaxSegmentsPerCell(builder, maxSegmentsPerCell): builder.PrependUint32Slot(2, maxSegmentsPerCell, 255)
def ConnectionGroupAddMaxSynapsesPerSegment(builder, maxSynapsesPerSegment): builder.PrependUint32Slot(3, maxSynapsesPerSegment, 255)
def ConnectionGroupAddBboxType(builder, bboxType): builder.PrependUint8Slot(4, bboxType, 0)
def ConnectionGroupAddBbox(builder, bbox): builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(bbox), 0)
def ConnectionGroupEnd(builder): return builder.EndObject()

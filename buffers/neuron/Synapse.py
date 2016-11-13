# automatically generated, do not modify

# namespace: neuron

import flatbuffers

class Synapse(object):
    __slots__ = ['_tab']

    # Synapse
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Synapse
    def PresynapticCellUID(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Synapse
    def Permanence(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0

    # Synapse
    def TerminalPositionType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

# ///used in cases when cell is lost
    # Synapse
    def TerminalPosition(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            from flatbuffers.table import Table
            obj = Table(bytearray(), 0)
            self._tab.Union(obj, o)
            return obj
        return None

    # Synapse
    def Overlaps(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # Synapse
    def OverlapsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def SynapseStart(builder): builder.StartObject(5)
def SynapseAddPresynapticCellUID(builder, presynapticCellUID): builder.PrependUint64Slot(0, presynapticCellUID, 0)
def SynapseAddPermanence(builder, permanence): builder.PrependFloat32Slot(1, permanence, 0)
def SynapseAddTerminalPositionType(builder, terminalPositionType): builder.PrependUint8Slot(2, terminalPositionType, 0)
def SynapseAddTerminalPosition(builder, terminalPosition): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(terminalPosition), 0)
def SynapseAddOverlaps(builder, overlaps): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(overlaps), 0)
def SynapseStartOverlapsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def SynapseEnd(builder): return builder.EndObject()

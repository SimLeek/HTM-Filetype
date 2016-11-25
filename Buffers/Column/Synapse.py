# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Column

import flatbuffers

class Synapse(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsSynapse(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Synapse()
        x.Init(buf, n + offset)
        return x

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
        return 0.0

    # Synapse
    def Overlaps(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # Synapse
    def OverlapsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def SynapseStart(builder): builder.StartObject(3)
def SynapseAddPresynapticCellUID(builder, presynapticCellUID): builder.PrependUint64Slot(0, presynapticCellUID, 0)
def SynapseAddPermanence(builder, permanence): builder.PrependFloat32Slot(1, permanence, 0.0)
def SynapseAddOverlaps(builder, overlaps): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(overlaps), 0)
def SynapseStartOverlapsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def SynapseEnd(builder): return builder.EndObject()
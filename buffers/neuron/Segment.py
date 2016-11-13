# automatically generated, do not modify

# namespace: neuron

import flatbuffers

class Segment(object):
    __slots__ = ['_tab']

    # Segment
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Segment
    def Synapses(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .Synapse import Synapse
            obj = Synapse()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Segment
    def SynapsesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Segment
    def LastUsedIteration(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

def SegmentStart(builder): builder.StartObject(2)
def SegmentAddSynapses(builder, synapses): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(synapses), 0)
def SegmentStartSynapsesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def SegmentAddLastUsedIteration(builder, lastUsedIteration): builder.PrependUint32Slot(1, lastUsedIteration, 0)
def SegmentEnd(builder): return builder.EndObject()

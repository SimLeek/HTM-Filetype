# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2014-2016, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

from Segment import Segment

class CellData(object):
    """ Class containing cell information. Internal to the connections. """

    __slots__ = ["_segments", "_lastUsedIteration", "_connectionGroup"]

    def __init__(self, last_used_iteration, connection_group):
        self._segments = []
        self._lastUsedIteration = last_used_iteration
        self._connectionGroup = connection_group

    def destroy(self):
        for segment in self._segments:
            segment.destroy()

        del self._connectionGroup._cells[self]

    def _leastRecentlyUsedSegment(self):
        """ Find this cell's segment that was least recently used.
        Implement this explicitly to make sure that tie-breaking is consistent.
        When there's a tie, choose the oldest segment.
        @param cell (int) Cell to query.
        @return (Object) Least recently used segment.
        """
        minSegment = None
        minIteration = float("inf")

        for segment in self._segments:
            if segment._lastUsedIteration < minIteration:
                minSegment = segment
                minIteration = segment._lastUsedIteration

        assert minSegment is not None

        return minSegment

    def createSegment(self, iteration):
        """ Adds a new segment on a cell.
        @param cell (int) Cell index
        @return (int) New segment index
        """
        while len(self._segments) >= self._connectionGroup.maxSegmentsPerCell:
            self._leastRecentlyUsedSegment()

        if len(self._connectionGroup._freeUIDs) > 0:
            UID = self._connectionGroup._freeUIDs.pop()
        else:
            UID = self._connectionGroup._nextUID
            self._connectionGroup._segmentForUID[UID] = None
            self._connectionGroup._nextUID += 1

        ordinal = self._connectionGroup._nextSegmentOrdinal
        self._connectionGroup._nextSegmentOrdinal += 1

        segment = Segment(self, UID, iteration, ordinal)
        self._segments.append(segment)
        self._connectionGroup._segmentForUID[UID] = segment

        return segment

    def recordActivity(self, iteration):
        self._lastUsedIteration = iteration

    def write(self, proto, UID, loc):
        """ Writes serialized data from cells to proto objects

        @param proto (DynamicStructBuilder) Proto object"""

        protoCell = proto.init('cell')

        proto.lastUsedIteration = self._lastUsedIteration
        proto.UID = UID
        protoLoc = protoCell.init('loc', len(loc))
        for j, pos in enumerate(loc):
            protoLoc[j] = pos

        segments = self._segments
        protoSegments = protoCell.init('segments', len(segments))

        for j, segment in enumerate(segments):
            synapses = segment._synapses
            protoSynapses = protoSegments[j].init('synapses', len(synapses))
            protoSegments[j].destroyed = False
            protoSegments[j].lastUsedIteration = segment._lastUsedIteration

            for k, synapse in enumerate(sorted(synapses, key=lambda s: s._ordinal)):
                protoSynapses[k].presynapticCell = synapse.presynapticCell
                protoSynapses[k].permanence = synapse.permanence
                protoSynapses[k].destroyed=False

    @classmethod
    def read(cls, proto, super):
        """ Reads deserialized data from proto object
        @param proto (DynamicStructBuilder) Proto object
        @return (CellData) CellData instance
        """
        # pylint: disable=W0212

        protoCell = cls(proto.lastUsedIteration)
        protoSegments = proto.segments

    def __eq__(self, other):
        """This should be used in combination with r-tree locations,
        as this class is used in combination with r-tree points."""

        return((sorted(self._segments, key=lambda x: x._ordinal) ==
                sorted(other._synapses, key=lambda x: x._ordinal)))
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

from Util.Constants import EPSILON
from Synapse import Synapse

class Segment(object):
    """ Class containing minimal information to identify a unique segment"""

    __slots__ = ["cell", "UID", "__synapses", "_lastUsedIteration", "_ordinal", "_connectionGroup"]

    def __init__(self, cell, UID, lastUsedIteration, ordinal, connection_group):
        """
        @param cell (int)
        UID of the cell that this segment is on.

        @param UID (int)
        This segments unique identifier.

        @param ordinal (long)
        Used to sort segments. The sort order needs to be consistent between
        implementations so that tie-breaking is consistent when finding the best
        matching segment. (needed?)
        """

        self.cell = cell
        self.UID = UID
        self.__synapses = set()
        self._lastUsedIteration = lastUsedIteration
        self._ordinal = ordinal
        self._connectionGroup = connection_group

    def destroy(self):
        """ Destroys a segment.
        @param segment (Object) Segment object representing the segment to be
                                destroyed
        """
        # Remove the synapses from all data structures outside this Segment.
        for synapse in self.__synapses:
            self._connectionGroup._removeSynapseFromPresynapticMap(synapse)
        self._connectionGroup._numSynapses -= len(segment._synapses)

        # Remove the segment from the cell's list.
        segments = self.cell._segments
        i = segments.index(self)
        del segments[i]

        # Free the flatIdx and remove the final reference so the Segment can be
        # garbage-collected.
        self._connectionGroup._freeUIDs.append(self.UID)
        self._connectionGroup._segmentForUID[self.UID] = None


    def _minPermanenceSynapse(self):
        """ Find this segment's synapse with the smallest permanence.
        This method is NOT equivalent to a simple min() call. It uses an EPSILON to
        account for floating point differences between C++ and Python.
        @param segment (Object) Segment to query.
        @return (Object) Synapse with the minimal permanence
        Note: On ties it will choose the first occurrence of the minimum permanence.
        """
        minSynapse = None
        minPermanence = float("inf")

        for synapse in sorted(self.__synapses,
                              key=lambda s: s._ordinal):
            if synapse.permanence < minPermanence - EPSILON:
                minSynapse = synapse
                minPermanence = synapse.permanence

        assert minSynapse is not None

        return minSynapse

    def createSynapse(self, presynapticCell, permanence, nextSynapseOrdinal):
        """ Creates a new synapse on a segment.
        @param segment         (Object) Segment object for synapse to be synapsed to
        @param presynapticCell (int)    Source cell index
        @param permanence      (float)  Initial permanence
        @return (Object) created Synapse object
        """

        while len(self.__synapses) >= self._connectionGroup.maxSynapsesPerSegment:
            self._minPermanenceSynapse().destroy()

        idx = len(self.__synapses)
        synapse = Synapse(self, presynapticCell, permanence, nextSynapseOrdinal, self._connectionGroup)

        self.__synapses.add(synapse)

        self._connectionGroup._synapsesForPresynapticCell[presynapticCell].add(synapse)

        self._connectionGroup._incrementNumSynapses()

        return synapse


    def recordActivity(self, iteration):
        self._lastUsedIteration = iteration

    def positionSortKey(self, nextSegmentOrdinal):
        """ Return a numeric key for sorting this segment.
        This can be used with `sorted`.
        @param segment
        A Segment within this Connections.
        @retval (float) A numeric key for sorting.
        """
        return self.cell + (self._ordinal / float(nextSegmentOrdinal))

    def __eq__(self, other):
        """This should be used in combination with r-tree locations,
        as this class is used in combination with r-tree points."""

        return(self.cell == other.cell and
               self._lastUsedIteration == other._lastUsedIteration and
               (sorted(self.__synapses, key=lambda x: x._ordinal) ==
                sorted(other.__synapses, key=lambda x: x._ordinal)))
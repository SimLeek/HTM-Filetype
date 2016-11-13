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

from bisect import bisect_left
from collections import defaultdict
from n_d_point_field import n_dimensional_n_split, n_dimensional_n_split_float

#note: generate UIDs as randint(min_int,max_int) and check if in hash_table

EPSILON = 0.00001 #constant error threshold

class Segment(object):
    """ Class containing minimal information to identify a unique segment"""

    __slots__ = ["cell", "UID", "_synapses", "_lastUsedIteration", "_ordinal"]

    def __init__(self, cell, UID, lastUsedIteration, ordinal):
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
        self._synapses = set()
        self._lastUsedIteration = lastUsedIteration
        self._ordinal = ordinal

    def __eq__(self, other):
        """This should be used in combination with r-tree locations,
        as this class is used in combination with r-tree points."""

        return(self.cell == other.cell and
               self._lastUsedIteration == other._lastUsedIteration and
               (sorted(self._synapses, key=lambda x: x._ordinal) ==
                sorted(other._synapses, key=lambda x: x._ordinal)))

class Synapse(object):
    """ Class containing minimal information to identify a unique synapse """

    __slots__ = ["segment", "presynapticCell", "permanence", "_ordinal"]

    def __init__(self, segment, presynapticCell, permanence, ordinal):
        """
        @param segment (object)
        Segment object that the synapse is synapsed to.

        @param presynapticCell (int)
        UID of the presynaptic cell of the synapse.

        param ordinal (long)
        Used to sort synapses. The sort order needs to be consistent between
        implementations so that tie-breaking is consistent when finding the min
        permanence synapse.
        """

        self.segment = segment
        self.presynapticCell = presynapticCell
        self.permanence = permanence
        self._ordinal = ordinal

    def __eq__(self, other):
        """ Explicitly implement this for unit testing. Allow floating point
        differences for synapse permanence.
        """
        return (self.segment.cell == other.segment.cell and
                self.presynapticCell == other.presynapticCell and
                abs(self.permanence - other.permanence) < EPSILON)

class CellData(object):
    """ Class containing cell information. Internal to the connections. """

    __slots__ = ["_segments", "_lastUsedIteration"]

    def __init__(self, lastUsedIteration = 0):
        self._segments = []
        self._lastUsedIteration = lastUsedIteration

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



def binSearch(arr, val):
  """ function for running binary search on a sorted list.
  @param arr (list) a sorted list of integers to search
  @param val (int)  a integer to search for in the sorted array
  @return (int) the index of the element if it is found and -1 otherwise.
  """
  i = bisect_left(arr, val)
  if i != len(arr) and arr[i] == val:
    return i
  return -1

class Connections(object):
    """ Class to hold data representing the connectivity of a collection of cells. """

    def __init__(self,
                 numCells,
                 bbox,
                 maxSegmentsPerCell = 255,
                 maxSynapsesPerSegment = 255,
                 locationType = "int",
                 UID=0):
        """ @param numCells (int) Number of cells in collection """

        #save member variables
        self.numCells = numCells
        assert maxSegmentsPerCell > 0
        assert maxSynapsesPerSegment > 0
        self.maxSegmentsPerCell = maxSegmentsPerCell
        self.maxSynapsesPerSegment = maxSynapsesPerSegment

        if locationType=="int":
            self._cellLocations = n_dimensional_n_split(bbox, numCells)
        elif locationType=="float":
            self._cellLocations = n_dimensional_n_split_float(bbox, numCells, CellData())

        points = ((self._cellLocations.intersection(bbox, objects=True)))

        # check if defaultdict is useful here (need dict and not set dui to calling via UIDs)
        # keeping dict in addition to r-tree because O(1) access/storage vs O(log_2(n))
        #todo: takes too long!
        self._cells = dict([(point.id, CellData()) for point in points])

        self._synapsesForPresynapticCell = defaultdict(set)
        self._segmentForUID = dict()
        self.cellUIDcounter = numCells

        self._numSynapses = 0
        self._freeUIDs = []
        self._nextUID = 0
        self._iteration = 0

        # Whenever creating a new Synapse or Segment, give it a unique ordinal.
        # These can be used to sort synapses or segments by age.
        self._nextSynapseOrdinal = long(0)
        self._nextSegmentOrdinal = long(0)

    #def createCell
    #def destroyCell

    def segmentsForCell(self, cell):
        """ Returns the segments that belong to a cell.

        @param cell (int) Cell UID

        @return (list)
        Segment objects representing segments on the given cell.
        """

        return self._cells[cell]._segments

    def synapsesForSegment(self, segment):
        """ Returns the synapses on a segment.
        @param segment (int) Segment index
        @return (set)
        Synapse objects representing synapses on the given segment.
        """

        return segment._synapses

    def dataForSynapse(self, synapse):
        """ Returns the data for a synapse.
        This method exists to match the interface of the C++ Connections. This
        allows tests and tools to inspect the connections using a common interface.
        @param synapse (Object) Synapse object
        @return Synapse data
        """
        return synapse

    def dataForSegment(self, segment):
        """ Returns the data for a segment.
        This method exists to match the interface of the C++ Connections. This
        allows tests and tools to inspect the connections using a common interface.
        @param synapse (Object) Segment object
        @return segment data
        """
        return segment

    def getSegment(self, cell, idx):
        """ Returns a Segment object of the specified segment using data from the
            self._cells array.
        @param cell (int) cell index
        @param idx  (int) segment index on a cell
        @return (Segment) Segment object with index idx on the specified cell
        """

        return self._cells[cell]._segments[idx]

    def _leastRecentlyUsedSegment(self, cell):
        """ Find this cell's segment that was least recently used.
        Implement this explicitly to make sure that tie-breaking is consistent.
        When there's a tie, choose the oldest segment.
        @param cell (int) Cell to query.
        @return (Object) Least recently used segment.
        """
        minSegment = None
        minIteration = float("inf")

        for segment in self.segmentsForCell(cell):
            if segment._lastUsedIteration < minIteration:
                minSegment = segment
                minIteration = segment._lastUsedIteration

        assert minSegment is not None

        return minSegment

    def _minPermanenceSynapse(self, segment):
        """ Find this segment's synapse with the smallest permanence.
        This method is NOT equivalent to a simple min() call. It uses an EPSILON to
        account for floating point differences between C++ and Python.
        @param segment (Object) Segment to query.
        @return (Object) Synapse with the minimal permanence
        Note: On ties it will choose the first occurrence of the minimum permanence.
        """
        minSynapse = None
        minPermanence = float("inf")

        for synapse in sorted(self.synapsesForSegment(segment),
                              key=lambda s: s._ordinal):
            if synapse.permanence < minPermanence - EPSILON:
                minSynapse = synapse
                minPermanence = synapse.permanence

        assert minSynapse is not None

        return minSynapse

    def segmentForUID(self, flatIdx):
        """ Get the segment with the specified flatIdx.
        @param flatIdx (int) The segment's flattened dict index.
        @return (Segment) segment object
        """
        return self._segmentForUID[flatIdx]

    def segmentFlatListLength(self):
        """ Get larger than the needed length for a list to hold a value for every segment's
        UID.
        @return (int) Required list length

        Mostly deprecated due to dict usage, but useful for high perormance applications like gpu
        """
        return self._nextUID

    def synapsesForPresynapticCell(self, presynapticCell):
        """ Returns the synapses for the source cell that they synapse on.
        @param presynapticCell (int) Source cell index
        @return (set) Synapse objects
        """
        return self._synapsesForPresynapticCell[presynapticCell]

    def numSegments(self, cell=None):
        """ Returns the number of segments.
        @param cell (int) optional parameter to get the number of segments on a cell
        @retval (int) number of segments on all cells if cell is not specified,
                      or on a specific specified cell
        """
        if cell is not None:
            return len(self._cells[cell]._segments)

        return self._nextUID - len(self._freeUIDs)

    def _removeSynapseFromPresynapticMap(self, synapse):
        inputSynapses = self._synapsesForPresynapticCell[synapse.presynapticCell]

        inputSynapses.remove(synapse)

        if len(inputSynapses) == 0:
            del self._synapsesForPresynapticCell[synapse.presynapticCell]

    def destroySegment(self, segment):
        """ Destroys a segment.
        @param segment (Object) Segment object representing the segment to be
                                destroyed
        """
        # Remove the synapses from all data structures outside this Segment.
        for synapse in segment._synapses:
            self._removeSynapseFromPresynapticMap(synapse)
        self._numSynapses -= len(segment._synapses)

        # Remove the segment from the cell's list.
        segments = self._cells[segment.cell]._segments
        i = segments.index(segment)
        del segments[i]

        # Free the flatIdx and remove the final reference so the Segment can be
        # garbage-collected.
        self._freeUIDs.append(segment.UID)
        self._segmentForUID[segment.UID] = None

    def createSegment(self, cell):
        """ Adds a new segment on a cell.
        @param cell (int) Cell index
        @return (int) New segment index
        """
        while self.numSegments(cell) >= self.maxSegmentsPerCell:
            self.destroySegment(self._leastRecentlyUsedSegment(cell))

        cellData = self._cells[cell]

        if len(self._freeUIDs) > 0:
            UID = self._freeUIDs.pop()
        else:
            UID = self._nextUID
            self._segmentForUID[UID] = None
            self._nextUID += 1

        ordinal = self._nextSegmentOrdinal
        self._nextSegmentOrdinal += 1

        segment = Segment(cell, UID, self._iteration, ordinal)
        cellData._segments.append(segment)
        self._segmentForUID[UID] = segment

        return segment

    def numSynapses(self, segment=None):
        """ Returns the number of Synapses.
        @param segment (Object) optional parameter to get the number of synapses on
                                a segment
        @retval (int) number of synapses on all segments if segment is not
                      specified, or on a specified segment
        """
        if segment is not None:
            return len(segment._synapses)
        return self._numSynapses

    def destroySynapse(self, synapse):
        """ Destroys a synapse.
        @param synapse (Object) Synapse object to destroy
        """

        self._numSynapses -= 1

        self._removeSynapseFromPresynapticMap(synapse)

        synapse.segment._synapses.remove(synapse)

    def createSynapse(self, segment, presynapticCell, permanence):
        """ Creates a new synapse on a segment.
        @param segment         (Object) Segment object for synapse to be synapsed to
        @param presynapticCell (int)    Source cell index
        @param permanence      (float)  Initial permanence
        @return (Object) created Synapse object
        """

        while self.numSynapses(segment) >= self.maxSynapsesPerSegment:
            self.destroySynapse(self._minPermanenceSynapse(segment))

        idx = len(segment._synapses)
        synapse = Synapse(segment, presynapticCell, permanence,
                          self._nextSynapseOrdinal)
        self._nextSynapseOrdinal += 1
        segment._synapses.add(synapse)

        self._synapsesForPresynapticCell[presynapticCell].add(synapse)

        self._numSynapses += 1

        return synapse

    def updateSynapsePermanence(self, synapse, permanence):
        """ Updates the permanence for a synapse.
        @param synapse    (Object) Synapse object to be updated
        @param permanence (float)  New permanence
        """

        synapse.permanence = permanence

    def computeActivity(self, activePresynapticCells, connectedPermanence):
        """ Compute each segment's number of active synapses for a given input.
        In the returned lists, a segment's active synapse count is stored at index
        `segment.UID`.
        @param activePresynapticCells (iter)  active cells
        @param connectedPermanence    (float) permanence threshold for a synapse
                                              to be considered connected
        @return (tuple) Contains:
                          `numActiveConnectedSynapsesForSegment`  (list),
                          `numActivePotentialSynapsesForSegment`  (list)
        """

        numActiveConnectedSynapsesForSegment = [0] * self._nextUID
        numActivePotentialSynapsesForSegment = [0] * self._nextUID

        threshold = connectedPermanence - EPSILON

        for cell in activePresynapticCells:
            for synapse in self._synapsesForPresynapticCell[cell]:
                UID = synapse.segment.UID
                numActivePotentialSynapsesForSegment[UID] += 1
                if synapse.permanence > threshold:
                    numActiveConnectedSynapsesForSegment[UID] += 1

        return (numActiveConnectedSynapsesForSegment,
                numActivePotentialSynapsesForSegment)

    def recordSegmentActivity(self, segment):
        """ Record the fact that a segment had some activity. This information is
            used during segment cleanup.
            @param segment The segment that had some activity.
        """
        segment._lastUsedIteration = self._iteration

    def recordCellActivity(self, cell):
        """ Record the fact that a cell had some activity. This information is
            used during cell cleanup.
            @param cell The UID of the cell that had some activity.
        """
        cell._lastUsedIteration = self._iteration

    def startNewIteration(self):
        """ Mark the passage of time. This information is used during segment
        cleanup.
        """
        self._iteration += 1

    def segmentPositionSortKey(self, segment):
        """ Return a numeric key for sorting this segment.
        This can be used with `sorted`.
        @param segment
        A Segment within this Connections.
        @retval (float) A numeric key for sorting.
        """
        return segment.cell + (segment._ordinal / float(self._nextSegmentOrdinal))

    def write(self, proto):
        """ Writes serialized data from cells to proto objects

        @param proto (DynamicStructBuilder) Proto object"""

        for i in xrange(len(self._cells)):
            protoCell = proto.init('cell', self.numCells)

            segments = self._cells[i]._segments
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

                proto.maxSegmentsPerCell = self.maxSegmentsPerCell
                proto.maxSynapsesPerSegment = self.maxSynapsesPerSegment
                proto.iteration = self._iteration
                proto.numCells = self.numCells

    @classmethod
    def read(cls, proto):
        """ Reads deserialized data from proto object
        @param proto (DynamicStructBuilder) Proto object
        @return (Connections) Connections instance
        """
        # pylint: disable=W0212
        protoCell = proto.cell
        connections = cls(len(protoCell),
                      proto.maxSegmentsPerCell,
                      proto.maxSynapsesPerSegment)

class Cluster(object):
    """Class to hold data about connected groups of neurons with different properties."""
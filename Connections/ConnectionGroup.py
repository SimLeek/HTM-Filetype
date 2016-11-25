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

from Columns.ColumnGroup import Column
from Columns.Util.Constants import EPSILON

from collections import defaultdict

import flatbuffers

import buffers.connectiongroup.BBox as BBox
import buffers.connectiongroup.ConnectionGroup as ConnectionGroup
import buffers.connectiongroup.FloatBBox as FloatBBox
import buffers.connectiongroup.IntBBox as IntBBox
import buffers.neuron.Cell as neuronCell
import buffers.neuron.FloatPos as FloatPos
import buffers.neuron.IntPos as IntPos
import buffers.neuron.Pos as posType
import buffers.neuron.Segment as CellSegment
import buffers.neuron.Synapse as CellSynapse
from n_d_point_field import n_dimensional_n_split, n_dimensional_n_split_float


# note: generate UIDs as randint(min_int,max_int) and check if in hash_table


class Connections(object):
    """ Class to hold data representing the connectivity of a collection of cells. """

    def __init__(self,
                 num_columns,
                 bbox,
                 max_cells_per_column=16,
                 max_segments_per_cell=255,
                 max_synapses_per_segment=255,
                 location_type="int",
                 uid=0,
                 start_with_no_neurons=False):
        """ @param num_columns (int) Number of cells in collection """

        # check argument validity
        assert max_cells_per_column > 0
        assert max_segments_per_cell > 0
        assert max_synapses_per_segment > 0
        assert isinstance(max_cells_per_column, int)
        assert isinstance(max_segments_per_cell, int)
        assert isinstance(max_synapses_per_segment, int)

        # save member variables
        self.numColumns = num_columns
        self.maxCellsPerColumn = max_cells_per_column
        self.maxSegmentsPerCell = max_segments_per_cell
        self.maxSynapsesPerSegment = max_synapses_per_segment

        # save class variables
        self.locationType = location_type
        self.UID = uid
        self.bbox = bbox

        if not start_with_no_neurons:
            if location_type == "int":
                self._columnLocations = n_dimensional_n_split(bbox, num_columns)
            elif location_type == "float":
                self._columnLocations = n_dimensional_n_split_float(bbox, num_columns)

            points = (self._columnLocations.intersection(bbox, objects=True))

            self._cells = dict([(point.id, Column(point.bbox, self)) for point in points])
            self.columnUIDcounter = num_columns
        else:

            self._columnLocations = n_dimensional_n_split(bbox, 0)

            self._cells = dict()
            self.columnUIDcounter = 0

        self._synapsesForPresynapticCell = defaultdict(set)
        self._segmentForUID = dict()

        self._numSynapses = 0
        self._freeUIDs = []
        self._nextUID = 0
        self._iteration = 0

        # Whenever creating a new Synapse or Segment, give it a unique ordinal.
        # These can be used to sort synapses or segments by age.
        self._nextSynapseOrdinal = long(0)
        self._nextSegmentOrdinal = long(0)

    def addColumn(self, columnUID, locationBBox):
        if self._cells[columnUID] == None:
            self._cells[columnUID] = column
        else:
            raise ValueError("Cell location already used.")

        self.columnUIDcounter = columnUID + 1
        self._columnLocations.insert(columnUID, locationBBox)

        self.numColumns += 1

    def addCellFromFile(self, filename):
        buf = open(filename, 'rb').read()
        buf = bytearray(buf)
        cell = neuronCell.Cell.GetRootAsCell(buf, 0)

        if cell.ConnectionsUID() != self.UID:
            raise RuntimeWarning(
                "Cell connections UID [" + str(cell.ConnectionsUID()) +
                "] does not match connections UID [" + str(self.UID) + "].")

        cellLocationBBox = None
        if cell.PositionType() == posType.Pos.FloatPos:
            if self.locationType != "float":
                raise ValueError(
                    "Neuron not of position type: " + self.locationType + ". Neuron may need to be projected.")
            pos_union = FloatPos.FloatPos()
            pos_union.Init(cell.Position().Bytes, cell.Position().Pos)

            cellLocationBBox = []

            for i in xrange(pos_union.CoordinatesLength()):
                cellLocationBBox.append(pos_union.Coordinates(i))

        elif cell.PositionType() == posType.Pos.IntPos:
            if self.locationType != "int":
                raise ValueError(
                    "Neuron not of position type: " + self.locationType + ". Neuron may need to be projected.")
            pos_union = FloatPos.FloatPos()
            pos_union.Init(cell.Position().Bytes, cell.Position().Pos)

            cellLocationBBox = []

            for i in xrange(pos_union.CoordinatesLength()):
                cellLocationBBox.append(pos_union.Coordinates(i))

        cellData = CellData(cellLocationBBox, cell.LastUsedIteration())
        self.addCell(cellData, cell.UID(), cellLocationBBox)

        # todo: add option for breaking class limits for max synapses/segments
        for i in xrange(cell.SegmentsLength()):

            self.createSegment(cell.UID())
            cellData._segments[-1]._lastUsedIteration = cell.Segments(i).LastUsedIteration()
            for j in xrange(cell.Segments(i).SynapsesLength()):
                syn = cell.Segments(i).Synapses(j)
                self.createSynapse(cellData._segments[-1], syn.PresynapticCellUID(), syn.Permanence())

    def writeCellToFile(self, cell, filename, destroy=True):
        builder = flatbuffers.Builder(0)

        # todo: refactor postype and other incorrectly cased includes
        loc, postype = None
        if self.locationType == "float":
            FloatPos.FloatPosStartCoordinatesVector(builder, len(self._cells[cell]._bbox))

            for i in reversed(range(0, len(self._cells[cell]._bbox))):
                builder.PrependFloat32(self._cells[cell]._bbox[i])
            loc = builder.EndVector(len(self._cells[cell]._bbox))
            postype = posType.Pos.FloatPos

        elif self.locationType == "int":
            IntPos.IntPosStartCoordinatesVector(builder, len(self._cells[cell]._bbox))

            for i in reversed(range(0, len(self._cells[cell]._bbox))):
                builder.PrependUint32(self._cells[cell]._bbox[i])
            loc = builder.EndVector(len(self._cells[cell]._bbox))
            postype = posType.Pos.IntPos

        segments = []
        for segment in self._cells[cell]._segments:
            synapses = []
            for synapse in segment._synapses:
                CellSynapse.SynapseStart(builder)
                CellSynapse.SynapseAddPresynapticCellUID(builder, synapse.presynapticCell)
                CellSynapse.SynapseAddPermanence(builder, synapse.permanence)
                synapses.append(CellSynapse.SynapseEnd(builder))

            CellSegment.SegmentStartSynapsesVector(builder, len(synapses))
            for i in reversed(range(0, len(synapses))):
                builder.PrependUOffsetTRelative(synapses[i])
            segmentSynapses = builder.EndVector(len(synapses))

            CellSegment.SegmentStart(builder)
            CellSegment.SegmentAddSynapses(builder, segmentSynapses)
            CellSegment.SegmentAddLastUsedIteration(builder, segment._lastUsedIteration)
            segments.append(CellSegment.SegmentEnd(builder))

        neuronCell.CellStartSegmentsVector(builder, len(segments))
        for i in reversed(range(0, len(segments))):
            builder.PrependUOffsetTRelative(segments[i])
        cellSegments = builder.EndVector(len(segments))

        neuronCell.CellStart(builder)
        neuronCell.CellAddPositionType(builder, postype)
        neuronCell.CellAddPosition(builder, loc)
        neuronCell.CellAddLastUsedIteration(builder, self._cells[cell]._lastUsedIteration)
        neuronCell.CellAddUID(builder, cell)
        neuronCell.CellAddConnectionsUID(builder, self.UID)
        neuronCell.CellAddSegments(builder, cellSegments)
        neuron = neuronCell.CellEnd(builder)

        builder.Finish(neuron)

        buf = builder.Output()
        open(filename, 'wb').write(buf)

        if destroy:
            self.destroyCell(cell)

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

    def segmentForUID(self, uid):
        """ Get the segment with the specified flatIdx.
        @param flatIdx (int) The segment's flattened dict index.
        @return (Segment) segment object
        """
        return self._segmentForUID[uid]

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

    def _decrementNumSynapses(self):
        self._numSynapses -= 1

    def _incrementNumSynapses(self):
        self._numSynapses += 1

    def _next_synapse_ordinal(self):
        self._nextSynapseOrdinal +=1
        return self._nextSynapseOrdinal-1

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

    def startNewIteration(self):
        """ Mark the passage of time. This information is used during segment
        cleanup.
        """
        self._iteration += 1

    def writeToFile(self, filename):
        """ Writes serialized data from group to flatbuffers

        @param filename (string) save file name/location"""

        builder = flatbuffers.Builder(0)

        bbox, bboxType = None
        if self.locationType == "float":
            FloatBBox.FloatBBoxStartCoordinatesVector(builder, len(self.bbox))

            for i in reversed(range(0, len(self.bbox))):
                builder.PrependFloat32(self.bbox[i])
            bbox = builder.EndVector(len(self.bbox))
            bboxType = BBox.BBox.FloatBBox

        elif self.locationType == "int":
            IntPos.IntPosStartCoordinatesVector(builder, len(self.bbox))

            for i in reversed(range(0, len(self.bbox))):
                builder.PrependUint32(self.bbox[i])
            bbox = builder.EndVector(len(self.bbox))
            bboxType = BBox.BBox.FloatBBox

        ConnectionGroup.ConnectionGroupStart(builder)
        ConnectionGroup.ConnectionGroupAddUID(builder, self.UID)
        ConnectionGroup.ConnectionGroupAddNumCells(builder, self.numColumns)
        ConnectionGroup.ConnectionGroupAddMaxSegmentsPerCell(builder, self.maxSegmentsPerCell)
        ConnectionGroup.ConnectionGroupAddMaxSynapsesPerSegment(builder, self.maxSynapsesPerSegment)
        ConnectionGroup.ConnectionGroupAddBboxType(builder, bboxType)
        ConnectionGroup.ConnectionGroupAddBbox(builder, bbox)
        connectionGroup = ConnectionGroup.ConnectionGroupEnd(builder)

        builder.Finish(connectionGroup)

        buf = builder.Output()
        # todo: force these to write correct extension names
        open(filename, 'wb').write(buf)

    @classmethod
    def readFromFile(cls, filename):
        """ Reads deserialized data from proto object
        @param proto (DynamicStructBuilder) Proto object
        @return (Connections) Connections instance
        """
        # pylint: disable=W0212

        buf = open(filename, 'rb').read()
        buf = bytearray(buf)
        connection_group = ConnectionGroup.ConnectionGroup.GetRootAsConnectionGroup(buf, 0)

        bbox = None
        locationType = None

        if connection_group.BboxType() == BBox.BBox.IntBBox:
            locationType = "int"
            bbox_union = IntBBox.IntBBox()
            bbox_union.Init(connection_group.Bbox().Bytes, connection_group.Bbox().Pos)
            bbox = []

            for i in xrange(bbox_union.CoordinatesLength()):
                bbox.append(bbox_union.Coordinates(i))

        elif connection_group.BboxType() == BBox.BBox.FloatBBox:
            locationType = "float"
            bbox_union = FloatBBox.FloatBBox()
            bbox_union.Init(connection_group.Bbox().Bytes, connection_group.Bbox().Pos)
            bbox = []

            for i in xrange(bbox_union.CoordinatesLength()):
                bbox.append(bbox_union.Coordinates(i))

        me = cls(
            connection_group.NumCells(),
            bbox,
            connection_group.MaxSegmentsPerCell(),
            connection_group.MaxSynapsesPerSegment(),
            locationType,
            connection_group.UID(),
            startWithNoNeurons=True)

        return me


class Cluster(object):
    """Class to hold data about connected groups of neurons with different properties."""

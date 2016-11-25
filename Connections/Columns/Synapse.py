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


class Synapse(object):
    """ Class containing minimal information to identify a unique synapse """

    __slots__ = ["segment", "presynaptic_cell", "permanence", "_ordinal", "_connectionGroup"]

    def __init__(self, segment, presynaptic_cell, permanence, ordinal, connection_group):
        """
        @param segment (object)
        Segment object that the synapse branches out from.

        @param presynaptic_cell (int)
        UID of the presynaptic cell the synapse receives input from/to.

        param ordinal (long)
        Used to sort synapses. The sort order needs to be consistent between
        implementations so that tie-breaking is consistent when finding the min
        permanence synapse.
        """

        self.segment = segment
        self.presynaptic_cell = presynaptic_cell
        self.permanence = permanence
        self._ordinal = ordinal
        self._connectionGroup = connection_group

    def updatePermanence(self, permanence):
        """ Updates the permanence for a synapse.
        @param synapse    (Object) Synapse object to be updated
        @param permanence (float)  New permanence
        """
        self.permanence = permanence

    def __eq__(self, other):
        """ Explicitly implement this for unit testing. Allow floating point
        differences for synapse permanence.
        """
        return (self.segment.cell == other.segment.cell and
                self.presynaptic_cell == other.presynapticCell and
                abs(self.permanence - other.permanence) < EPSILON)

    def destroy(self):
        self._connectionGroup._decrementNumSynapses()
        self._connectionGroup._removeSynapseFromPresynapticMap(self)
        self.segment._synapses.remove(self)

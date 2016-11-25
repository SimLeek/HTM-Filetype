from Cell import CellData

class Column(object):
    __slots__ = ["_cells", "_bbox", "_lastUsedIteration", "_connectionsGroup"]

    def __init__(self, bbox, connections_group, lastUsedIteration):
        self._cells = []
        self._bbox = bbox
        self._lastUsedIteration = lastUsedIteration
        self._connectionsGroup = connections_group

    def _leastRecentlyUsedCell(self):
        minCell = None
        minIteration = float("inf")

        for cell in self._cells:
            #todo: replace with accessor function
            if cell._lastUsedIteration < minIteration:
                minCell = cell
                minIteration = cell._lastUsedIteration

        assert minCell is not None

        return minCell

    def addCell(self, iteration):

        while len(self._cells) >= self._connectionsGroup.max_cells_per_column:
            self._leastRecentlyUsedCell().destroy()

        cell = CellData(iteration, self._connectionsGroup)
        self._cells.append(cell)

        return cell
#import HTMNeuron
import vtk

class vtk_points:
    #adapted from:
    # http://www.vtk.org/Wiki/VTK/Examples/Python/GeometricObjects/Display/Point
    def __init__(self):
        self.points = vtk.vtkPoints()
        self.vertices = vtk.vtkCellArray()

        self.point_colors = vtk.vtkUnsignedCharArray()
        self.point_colors.SetNumberOfComponents(3)
        self.point_colors.SetName("Colors")

        self.lines = vtk.vtkCellArray()

        self.line_colors = vtk.vtkUnsignedCharArray()
        self.line_colors.SetNumberOfComponents(3)
        self.line_colors.SetName("Colors")

    #def add_point(self, x, y, z):
    #    point = [x,y,z]
    #    self.add_point(point)

    def add_point(self, point, color):
        id = self.points.InsertNextPoint(point)
        self.vertices.InsertNextCell(1)
        self.vertices.InsertCellPoint(id)

        self.point_colors.InsertNextTupleValue(color)
        return id

    def add_line(self, point_a_index, point_b_index, color):
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, point_a_index)
        line.GetPointIds().SetId(1, point_b_index)

        id = self.lines.InsertNextCell(line)

        self.line_colors.InsertNextTupleValue(color)
        return id

    def set_poly_data(self):
        self.points_poly = vtk.vtkPolyData()
        self.points_poly.SetPoints(self.points)
        self.points_poly.SetVerts(self.vertices)

        self.points_poly.GetCellData().SetScalars(self.line_colors)

        self.lines_poly = vtk.vtkPolyData()
        self.lines_poly.SetPoints(self.points)
        self.lines_poly.SetLines(self.lines)

        self.lines_poly.GetCellData().SetScalars(self.line_colors)

    def visualize(self):
        point_mapper = vtk.vtkPolyDataMapper()
        line_mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            point_mapper.SetInput(self.points_poly)
            line_mapper.SetInput(self.lines_poly)
        else:
            point_mapper.SetInputData(self.points_poly)
            line_mapper.SetInputData(self.lines_poly)

        point_actor = vtk.vtkActor()
        line_actor = vtk.vtkActor()
        point_actor.SetMapper(point_mapper)
        line_actor.SetMapper(line_mapper)
        point_actor.GetProperty().SetPointSize(5)#todo: allow change point size
        #actor.GetProperty().SetPointColor

        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        renderer.AddActor(point_actor)
        renderer.AddActor(line_actor)

        renderer.SetBackground(.6,.6,.4)

        renderWindow.Render()
        renderWindowInteractor.Start()

if __name__ == "__main__":
    point_displayer = vtk_points()

    import randomSample

    for i in xrange(1000):
        x = randomSample.randInt(0, 1000, 4237842 + i)
        y = randomSample.randInt(0, 1000, 5437474 + i)
        z = randomSample.randInt(0, 1000, 6345876 + i)
        r = randomSample.randInt(0, 255, 7832495 + i)
        g = randomSample.randInt(0, 255, 7382132 + i)
        b = randomSample.randInt(0, 255, 5324875 + i)
        point_displayer.add_point([x,y,z], [r,g,b])

    line_a = randomSample.randomSample(xrange(0,500), 500, 432684)
    line_b = randomSample.randomSample(xrange(500, 1000), 500, 53245643)

    for i in range(len(line_a)):
        r = randomSample.randInt(0, 255, 5453476 + i)
        g = randomSample.randInt(0, 255, 5983279 + i)
        b = randomSample.randInt(0, 255, 9827312 + i)
        point_displayer.add_line(line_a[i], line_b[i], [r, g, b])

    point_displayer.set_poly_data()

    point_displayer.visualize()

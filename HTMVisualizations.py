#import HTMNeuron
import vtk

class vtk_points:
    #adapted from:
    # http://www.vtk.org/Wiki/VTK/Examples/Python/GeometricObjects/Display/Point
    def __init__(self):
        self.points = vtk.vtkPoints()
        self.vertices = vtk.vtkCellArray()

    def add_point(self, x, y, z):
        point = [x,y,z]
        self.add_point(point)

    def add_point(self, point):
        id = self.points.InsertNextPoint(point)
        self.vertices.InsertNextCell(1)
        self.vertices.InsertCellPoint(id)

    def set_poly_data(self):
        self.points_poly = vtk.vtkPolyData()
        self.points_poly.SetPoints(self.points)
        self.points_poly.SetVerts(self.vertices)

    def visualize(self):
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(self.points_poly)
        else:
            mapper.SetInputData(self.points_poly)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetPointSize(20)#todo: allow change point size
        actor.GetProperty().SetPointColor

        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        renderer.AddActor(actor)

        renderWindow.Render()
        renderWindowInteractor.Start()

if __name__ == "__main__":
    point_displayer = vtk_points()

    point_displayer.add_point([1.0, 2.0, 3.0])
    point_displayer.add_point([3.0, 2.0, 1.0])

    point_displayer.set_poly_data()

    point_displayer.visualize()

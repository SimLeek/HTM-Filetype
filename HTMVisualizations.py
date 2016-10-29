#import HTMNeuron
import vtk

global_keyDic = None

global_interactor_parent = None

global_camera = None
global_camera_renderWindow = None

class KeyPressInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, camera, renderWindow, parent = None):
        #should work with else statement, but doesnt for some reason

        global global_interactor_parent
        global_interactor_parent = vtk.vtkRenderWindowInteractor()
        if parent is not None:
            global_interactor_parent = parent

        global global_camera
        global_camera = camera

        global global_camera_renderWindow
        global_camera_renderWindow = renderWindow

        global global_keyDic
        global_keyDic = {
            'w': self._move_forward,
            's': self._move_backward,
            'a': self._yaw_left,
            'd': self._yaw_right,
            'Shift_L': self._pitch_up,
            'space': self._pitch_down
        }

        self.AddObserver("KeyPressEvent", self.keyPress)

    def _move_forward(self):
        #todo: change this to a velocity function with drag and let something else
        # interpolate the velocity over time
        norm = global_camera.GetViewPlaneNormal()
        pos = global_camera.GetPosition()
        global_camera.SetPosition(pos[0] - norm[0]*10,
                                  pos[1] - norm[1]*10,
                                  pos[2] - norm[2]*10)
        global_camera.SetFocalPoint(pos[0] - norm[0] * 20,
                                    pos[1] - norm[1] * 20,
                                    pos[2] - norm[2] * 20)

    def _move_backward(self):
        # todo: change this to a velocity function with drag and let something else
        # interpolate the velocity over time
        norm = global_camera.GetViewPlaneNormal()
        pos = global_camera.GetPosition()
        global_camera.SetPosition(pos[0] + norm[0] * 10,
                                  pos[1] + norm[1] * 10,
                                  pos[2] + norm[2] * 10)
        global_camera.SetFocalPoint(pos[0] - norm[0] * 20,
                                    pos[1] - norm[1] * 20,
                                    pos[2] - norm[2] * 20)

    def _yaw_right(self):
        global_camera.Yaw(-10)
        global_camera_renderWindow.GetInteractor().Render()

    def _yaw_left(self):
        global_camera.Yaw(10)
        global_camera_renderWindow.GetInteractor().Render()

    def _pitch_up(self):
        global_camera.Pitch(10)
        global_camera_renderWindow.GetInteractor().Render()

    def _pitch_down(self):
        global_camera.Pitch(-10)
        global_camera_renderWindow.GetInteractor().Render()


    def keyPress(self, obj, event):
        #self is lost. Gonna have to report this to vtk...
        key = global_interactor_parent.GetKeySym()


        if key in global_keyDic:
            global_keyDic[key]()
        else:
            print(key)

class vtk_triangle_strip:
    def __init__(self):
        self.points = vtk.vtkPoints()
        self.triangle_strip = vtk.vtkTriangleStrip()
        self.cells = vtk.vtkCellArray()
        self.cells.InsertMextCell(self.triangle_strip)
        self.polydata = vtk.vtkPolyData()
        self.polydata.SetPoints(self.points)
        self.polyData.SetStrips(self.cells)

        self.num_ids = 0

    def add_point(self, x, y, z):
        self.points.InsertNextPoint(x,y,z)
        self.num_ids = self.num_ids +1

        self.triangle_strip.GetPointIds().SetNumberOfIds(self.num_ids)
        self.triangle_strip.GetPointIds().SetId(self.num_ids - 1, self.num_ids - 1)

    def visualize(self):
        self.mapper = vtk.vtkDataSetMapper()
        if vtk.VTK_MAJOR_VERSION <=5:
            self.mapper.SetInput(self.polydata)
        else:
            self.mapper.SetInputData(self.polydata)

        actor = vtk.vtkActor()
        actor.SetMapper(self.mapper)
        actor.GetProperty().SetRepresentationToWireframe()

        # Create a renderer, render window, and interactor
        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        renderer.AddActor(actor)
        renderWindow.Render()
        renderWindowInteractor.Start()





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

        self.points_poly.GetPointData().SetScalars(self.point_colors)

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
        point_actor.GetProperty().SetPointSize(3)#todo: allow change point size
        #actor.GetProperty().SetPointColor

        renderer = vtk.vtkRenderer()

        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetInteractorStyle(
            KeyPressInteractorStyle(camera = renderer.GetActiveCamera(),
                                    renderWindow = renderWindow,
                                    parent = renderWindowInteractor)
        )
        renderWindowInteractor.SetRenderWindow(renderWindow)

        renderer.AddActor(point_actor)
        renderer.AddActor(line_actor)

        #light brown = .6,.6,.4
        # light brown = .2,.2,.1
        renderer.SetBackground(.6,.6,.4)

        renderWindow.Render()
        renderWindowInteractor.Start()

if __name__ == "__main__":
    point_displayer = vtk_points()

    import randomSample
    import math

    from opensimplex import OpenSimplex

    simp_r = OpenSimplex(seed=364)
    simp_g = OpenSimplex(seed=535)
    simp_b = OpenSimplex(seed=656)

    '''for i in xrange(100000):
        x = randomSample.rand_int(0, 1000, 4237842 + i)
        y = randomSample.rand_int(0, 1000, 5437474 + i)

        r1 = .0009765625 * (simp_g.noise2d(x=x, y=y))
        r2 = .001953125 * (simp_r.noise2d(x=x / 2.0, y=y / 2.0))
        r3 = .00390625 * (simp_b.noise2d(x=x / 4.0, y=y / 4.0,))
        r4 = .0078125 * (simp_g.noise2d(x=x / 8.0, y=y / 8.0))
        r5 = .015625 * (simp_r.noise2d(x=x / 16.0, y=y / 16.0))
        r6 = .03125 * (simp_b.noise2d(x=x / 32.0, y=y / 32.0))
        r7 = .0625 * (simp_g.noise2d(x=x / 64.0, y=y / 64.0))
        r8 = .125 * (simp_r.noise2d(x=x / 128.0, y=y / 128.0))
        r9 = .25 * (simp_b.noise2d(x=x / 256.0, y=y / 256.0))
        r10 = .5 * (simp_g.noise2d(x=x / 512.0, y=y / 512.0))
        r11 = (simp_r.noise2d(x=x / 1024.0, y=y / 1024.0))
        normalization_factor = .5
        val = ((r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9) / 2.0)
        if val > 0:
            p = 1.0
        else:
            p = -1.0
        norm_val = (abs(val) ** normalization_factor) * p
        pos_val = (norm_val + 1.0) / 2.0
        z = pos_val * 254.0

        point_displayer.add_point([x-100, y-100, z-100], [160, int(z), 20])
'''

    from n_d_point_field import n_dimensional_n_split_float
    split_pts = n_dimensional_n_split_float([0,1000,0,2, 0, 3], 345)

    for i in xrange(len(split_pts)/3):
        x = split_pts[i*3]
        y = split_pts[i*3 +1]
        z = split_pts[i*3 + 2]

        r = randomSample.randInt(0, 255, 5453476 + i)
        g = randomSample.randInt(0, 255, 5983279 + i)
        b = randomSample.randInt(0, 255, 9827312 + i)

        point_displayer.add_point([x, y, z], [r, g, b])

    '''for i in xrange(100000):


        x = randomSample.rand_int(0, 1000, 4237842 + i)
        y = randomSample.rand_int(0, 1000, 5437474 + i)
        z = randomSample.rand_int(0, 1000, 6345876 + i)

        d = math.sqrt((x-500)**2 + (y-500)**2 + (z-500)**2) / 500.0

        r1 = .0009765625*(simp_g.noise3d(x=x, y=y, z=z))
        r2 = .001953125*(simp_r.noise3d(x=x / 2.0, y=y / 2.0, z=z / 2.0))
        r3 = .00390625*(simp_b.noise3d(x=x / 4.0, y=y / 4.0, z=z / 4.0))
        r4 = .0078125*(simp_g.noise3d(x=x / 8.0, y=y / 8.0, z=z / 8.0))
        r5 = .015625*(simp_r.noise3d(x=x / 16.0, y=y / 16.0, z=z / 16.0))
        r6 = .03125*(simp_b.noise3d(x=x / 32.0, y=y / 32.0, z=z / 32.0))
        r7 = .0625*(simp_g.noise3d(x=x / 64.0, y=y / 64.0, z=z / 64.0))
        r8 = .125*(simp_r.noise3d(x=x / 128.0, y=y / 128.0, z=z / 128.0))
        r9 = .25*(simp_b.noise3d(x=x / 256.0, y=y / 256.0, z=z / 256.0))
        r10 = .5*(simp_g.noise3d(x=x / 512.0, y=y / 512.0, z=z / 512.0))
        r11 = (simp_r.noise3d(x=x / 1024.0, y=y / 1024.0, z=z / 1024.0))
        normalization_factor = .5
        val = ((r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9) / 2.0)
        if val>0:
            p=1.0
        else:
            p=-1.0

        #use ^d for cumulus clouds,
        #use distance from a certain height for a sky of clouds
        #use constant power <1 for endless 3d field of clouds
        #use distance from sets of points or lines for other shapes

        norm_val = (abs(val)**d)*p
        pos_val = (norm_val +1.0)/2.0
        r= int(pos_val*254.0)
        #r5 = int((r5)*255.0/2.0)
        #lim octaves->inf gives 1/2^x sum (=1)
        if r> 160:
            point_displayer.add_point([x,y,z], [r,r,r])'''



    '''line_a = randomSample.randomSample(xrange(0,500), 500, 432684)
    line_b = randomSample.randomSample(xrange(500, 1000), 500, 53245643)

    for i in range(len(line_a)):
        r = randomSample.rand_int(0, 255, 5453476 + i)
        g = randomSample.rand_int(0, 255, 5983279 + i)
        b = randomSample.rand_int(0, 255, 9827312 + i)
        point_displayer.add_line(line_a[i], line_b[i], [r, g, b])'''




    point_displayer.set_poly_data()

    point_displayer.visualize()

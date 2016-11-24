#HTM Filetype

A corruption tolerant filetype for saving neurogenesis/neurodegeneration enabled HTM neural networks

##Prerequisites

###For whole project

 * rtree:
   * Get from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#rtree)

Rtree sets up a tree of rectangles to sort all the n-dimensional points into. This makes it so individual points can be found in O(log_m(n)) time.

###For Testing and Visualization

 * Anaconda Python 2.7
   * Get 2.7 version from [here](https://www.continuum.io/downloads)
   * Set up in Pycharm via File->Settings->Project:[project name]->Project Interpreter
 * VTK
   * ` conda install -c anaconda vtk=6.3.0 `

Anaconda is useful for installing VTK. You could build VTK for python, but that's harder to do on Windows.

###Example output

####Point Field Test 1
![Point Field Test 1, all points arranged orderly in a box, save for a few outliers, which are also arranged somewhat orderly](https://i.imgur.com/O3uUNHT.png)

All points should be arranged in rows within prism, save for a few outliers, and colors should show linear order.

![Another point field test](https://i.imgur.com/rJ7g75f.png)

It's harder to see linear order when a lot of points are generated, but there should be several lines visible on some of the faces of the generated prism.
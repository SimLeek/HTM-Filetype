#HTM Filetype

A corruption tolerant filetype for saving neurogenesis/neurodegeneration enabled HTM neural networks

##Testing

For running the network, once it's implemented, no packages need to be installed. However, for testing and debugging, vtk is necessary for visualizations and unittest is necessary for unit testing.

###Example output

####Point Field Test 1
![Point Field Test 1, all points arranged orderly in a box, save for a few outliers, which are also arranged somewhat orderly](https://i.imgur.com/O3uUNHT.png)

All points should be arranged in rows within prism, save for a few outliers, and colors should show linear order.

![Another point field test](https://i.imgur.com/rJ7g75f.png)

It's harder to see linear order when a lot of points are generated, but there should be several lines visible on some of the faces of the generated prism.
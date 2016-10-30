import n_d_point_field as ndpf

import unittest

class split_test(unittest.TestCase):
    def test_n_split_points_int(self):
        points = ndpf.n_split_points(0, 20, 19)
        points_test = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        self.assertSequenceEqual(points,points_test)

        points = ndpf.n_split_points(-84, 137, 45)
        points_test = [-80, -76, -72, -68, -64, -60, -56, -52, -48, -44, -40, -36, -32, -28, -24, -20, -16, -12, -8,
                       -4, 0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88,
                       92, 96]
        self.assertSequenceEqual(points,points_test)

    def test_n_split_points_float(self):
        points = ndpf.n_split_points_float(0, 1, 17)
        test_points = [0.05555555555555555, 0.1111111111111111, 0.16666666666666666, 0.2222222222222222,
                       0.2777777777777778, 0.3333333333333333, 0.38888888888888884, 0.4444444444444444,
                       0.5, 0.5555555555555556, 0.611111111111111, 0.6666666666666666, 0.7222222222222222,
                       0.7777777777777777, 0.8333333333333333, 0.8888888888888888, 0.9444444444444444]
        self.assertSequenceEqual(points, test_points)

        points = ndpf.n_split_points_float(-10, 13, 28)
        test_points = [-9.206896551724139, -8.413793103448276, -7.620689655172414, -6.827586206896552,
                       -6.0344827586206895, -5.241379310344827, -4.448275862068965, -3.655172413793103,
                       -2.862068965517241, -2.068965517241379, -1.275862068965516, -0.4827586206896548,
                       0.3103448275862064, 1.1034482758620694, 1.8965517241379324, 2.6896551724137936,
                       3.482758620689655, 4.275862068965518, 5.068965517241381, 5.862068965517242,
                       6.655172413793103, 7.448275862068968, 8.24137931034483, 9.03448275862069,
                       9.827586206896552, 10.620689655172413, 11.413793103448278, 12.206896551724139]

        self.assertSequenceEqual(points, test_points)
        self.assertEqual(len(points), 28)

        points = ndpf.n_split_points_float(-.2, .2, 15437)
        self.assertEqual(len(points), 15437)

    def test_get_tiny_d_tip(self):
        tip = ndpf.get_tiny_d_tip([45,87,26.5], 1, 4.57)
        test_tip = 0.17

        self.assertAlmostEqual(tip, 0.17)

    def test_stuff_the_ds(self):
        field = ndpf.stuff_the_ds([0,100,-70,70], [100,140], 23)
        test_field = [15, -58, 15, -35, 15, -12, 15, 11, 15, 34, 15, 57, 38, -58, 38, -35, 38, -12, 38, 11, 38, 34,
                      38, 57, 61, -58, 61, -35, 61, -12, 61, 11, 61, 34, 61, 57, 84, -58, 84, -35, 84, -12, 84, 11,
                      84, 34, 84, 57]
        self.assertSequenceEqual(field, test_field)

    def test_stuff_the_ds_float(self):
        field = ndpf.stuff_the_ds_float([0, 100, -70, 70], [100, 140], 23.125)
        test_field = [15.3125, -57.8125, 15.3125, -34.6875, 15.3125, -11.5625, 15.3125, 11.5625, 15.3125, 34.6875,
                      15.3125, 57.8125, 38.4375, -57.8125, 38.4375, -34.6875, 38.4375, -11.5625, 38.4375, 11.5625,
                      38.4375, 34.6875, 38.4375, 57.8125, 61.5625, -57.8125, 61.5625, -34.6875, 61.5625, -11.5625,
                      61.5625, 11.5625, 61.5625, 34.6875, 61.5625, 57.8125, 84.6875, -57.8125, 84.6875, -34.6875,
                      84.6875, -11.5625, 84.6875, 11.5625, 84.6875, 34.6875, 84.6875, 57.8125]

        self.assertSequenceEqual(field, test_field)

    def test_get_d_lengths(self):
        lengths = ndpf.get_d_lengths([-25.5, 37, 0, 100])
        test_lengths = [62.5, 100]
        self.assertSequenceEqual(lengths, test_lengths)

    def test_get_d_thickness(self):
        thickness = ndpf.get_d_thickness([37, 100])
        test_thickness = 3700
        self.assertEqual(thickness, test_thickness)

    def test_pixel_blur_d_float(self):
        field = ndpf.pixel_blur_d_float([-27, 37, 0, 500,0,8, 0, 2], 10)
        test_field = [5.0, 52.010101267766686, 4.0, 1.0, 5.0, 108.57864376269049, 4.0, 1.0,
                      5.0, 165.1471862576143, 4.0, 1.0, 5.0, 221.7157287525381, 4.0, 1.0,
                      5.0, 278.2842712474619, 4.0, 1.0, 5.0, 334.8528137423857, 4.0, 1.0,
                      5.0, 391.4213562373095, 4.0, 1.0, 5.0, 447.9898987322333, 4.0, 1.0]

        self.assertSequenceEqual(field, test_field)

        field = ndpf.pixel_blur_d_float([-27, 37, 0, 500,0,10,0,1], 1000)
        self.assertLessEqual(len(field)/4,1000)



if __name__ == '__main__':
    unittest.main()
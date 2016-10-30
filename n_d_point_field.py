import math
from rng import *
import numbers

def n_split_points(min_val, max_val, n):
    step = int((max_val - min_val) / (n + 1))

    assert step > 0

    vals = []

    for distance in xrange(1, n + 1):
        vals.append(min_val + distance * step)

    return vals


def n_split_points_float(min_val, max_val, n):
    step = float(max_val - min_val) / (n + 1)

    vals = []

    for distance in xrange(1, n + 1):
        vals.append(min_val + distance * step)

    return vals


def get_tiny_d_tip(lengths, index, n_cube_len):
    big_d_length = lengths[index]
    assert isinstance(n_cube_len, numbers.Real)
    the_tip = big_d_length % n_cube_len

    return the_tip


def stuff_the_ds(min_max_array, lengths, distance_between_points):
    # n-dimensional space filling algorithm
    points = []
    for index in xrange(len(lengths)):
        offset = int((distance_between_points +
                      get_tiny_d_tip(lengths, index, distance_between_points)) / 2)
        new_points = []
        if index == 0:
            for j in xrange((lengths[index]) / distance_between_points):
                new_points.append(offset + min_max_array[index * 2] + distance_between_points * j)
        else:
            for j in xrange(len(points) / index):
                for k in xrange((lengths[index]) / distance_between_points):
                    for l in xrange(index):
                        new_points.append(points[j * index + l])
                    new_points.append(offset + min_max_array[index * 2] + distance_between_points * k)
        points = new_points

    return points


def stuff_the_ds_float(min_max_array, lengths, n_cube_len):
    # n-dimensional space filling algorithm
    points = []
    for index in xrange(len(lengths)):
        offset = (n_cube_len + get_tiny_d_tip(lengths, index, n_cube_len)) / 2
        new_points = []
        if index == 0:
            for j in xrange(int((lengths[index]) / n_cube_len)):
                new_points.append(offset + min_max_array[index * 2] + n_cube_len * j)
        else:
            for j in xrange(len(points) / index):
                for k in xrange(int(lengths[index] / n_cube_len)):
                    for l in xrange(index):
                        new_points.append(points[j * index + l])
                    new_points.append(offset + min_max_array[index * 2] + n_cube_len * k)
        points = new_points

    return points


def get_d_lengths(min_max_array):
    lengths = []

    for index in xrange(len(min_max_array) / 2):
        lengths.append(min_max_array[index * 2 + 1] - min_max_array[index * 2])

    return lengths


def get_d_thickness(lengths):
    vol = 1
    for index in xrange(len(lengths)):
        assert lengths[index] > 0
        vol = vol * lengths[index]
    return vol


def pixel_blur_d_float(min_max_array, n):
    if len(min_max_array) % 2 != 0 or len(min_max_array) == 0:
        raise IndexError("array is not correct size")

    lengths = get_d_lengths(min_max_array)

    thickness = get_d_thickness(lengths)
    tiny_d_cube_len = (thickness / n) ** (1.0 / (len(lengths)))
    index = 0
    deleted_indices = []
    deleted_lengths = []
    deleted_min_vals = []
    while index in xrange(len(lengths)):
        if lengths[index] < tiny_d_cube_len:
            deleted_indices.append(index+len(deleted_indices))
            deleted_lengths.append(lengths[index])
            del lengths[index]
            deleted_min_vals.append(min_max_array[index * 2])
            del min_max_array[index * 2]
            del min_max_array[index * 2]
            thickness = get_d_thickness(lengths)
            tiny_d_cube_len = (thickness / n) ** (1.0 / (len(lengths)))
            index = 0
        else:
            index += 1
    #next:store dimensions and add back using middles

    stuffed_ds = stuff_the_ds_float(min_max_array, lengths, tiny_d_cube_len)

    for index in xrange(len(deleted_indices)):
        new_ds = []
        d_index = deleted_indices[index]
        pos = deleted_lengths[index] / 2.0 + deleted_min_vals[index]
        prev_num_ds = len(lengths) + index
        for j in xrange(len(stuffed_ds)/prev_num_ds):
            new_ds.extend(stuffed_ds[prev_num_ds*j:prev_num_ds*j+d_index])
            new_ds.append(pos)
            new_ds.extend(stuffed_ds[prev_num_ds * j + d_index : prev_num_ds * j])

        stuffed_ds = new_ds

    return stuffed_ds

def pixel_blur_d(min_max_array, n):
    if len(min_max_array) % 2 != 0 or len(min_max_array) == 0:
        raise IndexError("array is not correct size")

    lengths = get_d_lengths(min_max_array)

    thickness = get_d_thickness(lengths)

    tiny_d_cube_len = int(math.ceil((thickness / n) ** (1.0 / (len(lengths)))))

    return stuff_the_ds(min_max_array, lengths, tiny_d_cube_len)


def unknown_length_sorted_array_2n_search_1(search_val, arr, pos, array_div=1):

    step = 1
    prev_pos = pos
    for index in xrange(array_div):
        try:
            if arr[pos * array_div + index] > search_val[index] and pos * array_div + index >= 0:
                while arr[pos * array_div + index] > search_val[index] and pos * array_div + index >= 0 \
                        and (index == 0 or arr[pos * array_div + index - 1] == search_val[index - 1]):
                    prev_pos = pos
                    pos -= step
                    step *= 2
            elif arr[pos * array_div + index] < search_val[index] and pos * array_div + index >= 0:
                while arr[pos * array_div + index] < search_val[index] and pos * array_div + index >= 0 \
                        and (index == 0 or arr[pos * array_div + index - 1] == search_val[index - 1]):
                    prev_pos = pos
                    pos = pos + step
                    step *= 2
            if arr[pos * array_div + index] != search_val[index]:
                break
            else:
                step = 1
        except IndexError:
            pass

    if pos < 0:
        pos = 0

    if (pos + 1) * array_div - 1 >= len(arr):
        pos = len(arr) / array_div - 1

    return prev_pos, pos


def order(first, second):
    if first > second:
        return second, first
    else:
        return first, second


def search_array_2n_contiguous_subset_axis_rightmost(search_val, arr, start, end, skip, axis):
    mid = int((end - start) / 2) + start

    while start != mid and mid != end:
        array_val = arr[mid * skip + axis]
        if search_val < array_val:
            end = mid
            mid = int((end - start) / 2) + start
        elif array_val <= search_val:
            start = mid
            mid = int((end - start) / 2) + start

    return mid


def search_array_2n_contiguous_subset_axis_leftmost(search_val, arr, start, end, skip, axis):
    mid = int((end - start) / 2) + start

    while start != mid and mid != end:
        array_val = arr[mid * skip + axis]
        if search_val <= array_val:
            end = mid
            mid = int((end - start) / 2) + start + 1
        elif array_val < search_val:
            start = mid
            mid = int((end - start) / 2) + start + 1

    return mid


def search_array_2n_contiguous_subset_axis_first_match(search_val, arr, start, end, skip, axis):
    mid = int((end - start) / 2) + start

    while start != mid and min != end:
        array_val = arr[mid * skip + axis]
        if search_val < array_val:
            end = mid
            mid = int((end - start) / 2) + start
        elif array_val < search_val:
            start = mid
            mid = int((end - start) / 2) + start + 1
        else:
            return mid, True

    if search_val < arr[mid * skip + axis]:
        return mid - 1, False
    return mid, False


def search_array_2n_contiguous_subset(search_arr, arr, bound_a, bound_b):
    start, end = order(bound_a, bound_b)
    skip = len(search_arr)

    for index in xrange(len(search_arr)):
        if index != len(search_arr) - 1:
            start = search_array_2n_contiguous_subset_axis_leftmost(search_arr[index], arr, start, end, skip, index)
            end = search_array_2n_contiguous_subset_axis_rightmost(search_arr[index], arr, start, end, skip, index)
            if start == end:
                return (start - 1), False
        else:
            return search_array_2n_contiguous_subset_axis_first_match(search_arr[index], arr, start, end, skip, index)


def n_dimensional_midpoint(point1, point2):
    midpoint = []

    for index in xrange(len(point1)):
        dist = abs(point1[index] - point2[index])
        min_pt = min(point1[index], point2[index])
        midpoint.append(int(min_pt + dist / 2.0))

    return midpoint


def n_dimensional_n_split(min_max_array, n):
    tiny_ds = pixel_blur_d(min_max_array, n)

    dimensions = (len(min_max_array) / 2)

    tiny_ds_per_big_d = len(tiny_ds) / dimensions

    while tiny_ds_per_big_d < n:
        n -= tiny_ds_per_big_d

        more_pts = pixel_blur_d(min_max_array, n)
        for index in xrange(len(more_pts) / dimensions):
            pt = []
            for j in xrange(dimensions):
                pt.append(more_pts[index * dimensions + j])
            duplicate_loc, found = search_array_2n_contiguous_subset(pt, tiny_ds, 0, tiny_ds_per_big_d)

            if not found:
                new_tiny_ds = tiny_ds[0:duplicate_loc * n + n - 1]
                new_tiny_ds.extend(pt)
                new_tiny_ds.extend(tiny_ds[duplicate_loc * n + n:-1])
                tiny_ds = new_tiny_ds
            else:
                if duplicate_loc != tiny_ds_per_big_d:
                    next_pt = []
                    for j in xrange(n):
                        next_pt.append(tiny_ds[(duplicate_loc + 1) * dimensions + j])
                    replacement_pt = n_dimensional_midpoint(pt, next_pt)
                    tiny_ds.extend(replacement_pt)
                else:
                    next_pt = []
                    for j in xrange(n):
                        next_pt.append(tiny_ds[(duplicate_loc - 1) * dimensions + j])
                    replacement_pt = n_dimensional_midpoint(pt, next_pt)
                    tiny_ds.extend(replacement_pt)
                new_tiny_ds = tiny_ds[0:duplicate_loc * n + n - 1]
                new_tiny_ds.extend(replacement_pt)
                new_tiny_ds.extend(tiny_ds[duplicate_loc * n + n:-1])
                tiny_ds = new_tiny_ds

        tiny_ds_per_big_d = len(tiny_ds) / (len(min_max_array) / 2)

    return tiny_ds


def n_dimensional_n_split_float(min_max_array, n):
    tiny_ds = pixel_blur_d_float(min_max_array, n)

    dimensions = (len(min_max_array) / 2)

    tiny_ds_per_big_d = len(tiny_ds) / dimensions

    while tiny_ds_per_big_d < n:
        n -= tiny_ds_per_big_d

        more_pts = pixel_blur_d_float(min_max_array, n)
        for index in xrange(len(more_pts) / dimensions):
            pt = []
            for j in xrange(dimensions):
                pt.append(more_pts[index * dimensions + j])
            duplicate_loc, found = search_array_2n_contiguous_subset(pt, tiny_ds, 0, tiny_ds_per_big_d)

            if not found:
                new_tiny_ds = tiny_ds[0:duplicate_loc * n + n - 1]
                new_tiny_ds.extend(pt)
                new_tiny_ds.extend(tiny_ds[duplicate_loc * n + n:-1])
                tiny_ds = new_tiny_ds
            else:
                if duplicate_loc != tiny_ds_per_big_d:
                    next_pt = []
                    for j in xrange(n):
                        next_pt.append(tiny_ds[(duplicate_loc + 1) * dimensions + j])
                    replacement_pt = n_dimensional_midpoint(pt, next_pt)
                    tiny_ds.extend(replacement_pt)
                else:
                    next_pt = []
                    for j in xrange(n):
                        next_pt.append(tiny_ds[(duplicate_loc - 1) * dimensions + j])
                    replacement_pt = n_dimensional_midpoint(pt, next_pt)
                    tiny_ds.extend(replacement_pt)
                new_tiny_ds = tiny_ds[0:duplicate_loc * n + n - 1]
                new_tiny_ds.extend(replacement_pt)
                new_tiny_ds.extend(tiny_ds[duplicate_loc * n + n:-1])
                tiny_ds = new_tiny_ds

        tiny_ds_per_big_d = len(tiny_ds) / (len(min_max_array) / 2)

    return tiny_ds


if __name__ == "__main__":

    field = pixel_blur_d_float([-27, 37, 0, 500,0,8, 0, 2], 10)
    print(field)
    '''maximum = 9223372036854775807
    minimum = 0

    test_array = []
    for i in xrange(100):
        test_array.append(rand_int(0, 10000, 48736489723 + i))

    test_array.sort()

    test_array = n_dimensional_n_split([0, 100, 0, 100], 100)

    print("test_array:", test_array)

    a, b = unknown_length_sorted_array_2n_search_1([65, 95], test_array, 50, 2)
    print("alg:", a, b)
    print("arr a:", test_array[2 * a], test_array[2 * a + 1])
    print("arr b:", test_array[2 * b], test_array[2 * b + 1])

    # loc = search_array_2n_contiguous_subset([65,85], test_array, 0, 100)
    split = n_dimensional_n_split_float([0, 100, 0, 100], 137)

    print(split)'''

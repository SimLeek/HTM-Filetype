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
    min_max_copy = min_max_array[:]

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
            deleted_min_vals.append(min_max_copy[index * 2])
            del min_max_copy[index * 2]
            del min_max_copy[index * 2]
            thickness = get_d_thickness(lengths)
            tiny_d_cube_len = (thickness / n) ** (1.0 / (len(lengths)))
            index = 0
        else:
            index += 1
    #next:store dimensions and add back using middles

    stuffed_ds = stuff_the_ds_float(min_max_copy, lengths, tiny_d_cube_len)

    for index in xrange(len(deleted_indices)):
        new_ds = []
        d_index = deleted_indices[index]
        pos = deleted_lengths[index] / 2.0 + deleted_min_vals[index]
        prev_num_ds = len(lengths) + index
        for j in xrange(len(stuffed_ds)/prev_num_ds):
            new_ds.extend(stuffed_ds[prev_num_ds*j:prev_num_ds*j+d_index])
            new_ds.append(pos)
            new_ds.extend(stuffed_ds[prev_num_ds * j + d_index : prev_num_ds * (j+1)])

        stuffed_ds = new_ds

    return stuffed_ds

def pixel_blur_d(min_max_array, n):
    if len(min_max_array) % 2 != 0 or len(min_max_array) == 0:
        raise IndexError("array is not correct size")

    lengths = get_d_lengths(min_max_array)
    min_max_copy = min_max_array[:]

    thickness = get_d_thickness(lengths)

    tiny_d_cube_len = int(math.ceil((thickness / n) ** (1.0 / (len(lengths)))))
    index = 0
    deleted_indices = []
    deleted_lengths = []
    deleted_min_vals = []
    while index in xrange(len(lengths)):
        if lengths[index] < tiny_d_cube_len:
            deleted_indices.append(index + len(deleted_indices))
            deleted_lengths.append(lengths[index])
            del lengths[index]
            deleted_min_vals.append(min_max_copy[index * 2])
            del min_max_copy[index * 2]
            del min_max_copy[index * 2]
            thickness = get_d_thickness(lengths)
            tiny_d_cube_len = int(math.ceil((thickness / n) ** (1.0 / (len(lengths)))))
            index = 0
        else:
            index += 1

    stuffed_ds = stuff_the_ds(min_max_copy, lengths, tiny_d_cube_len)

    for index in xrange(len(deleted_indices)):
        new_ds = []
        d_index = deleted_indices[index]
        pos = deleted_lengths[index] / 2 + deleted_min_vals[index]
        prev_num_ds = len(lengths) + index
        for j in xrange(len(stuffed_ds)/prev_num_ds):
            new_ds.extend(stuffed_ds[prev_num_ds*j:prev_num_ds*j+d_index])
            new_ds.append(pos)
            new_ds.extend(stuffed_ds[prev_num_ds * j + d_index : prev_num_ds * (j+1)])

        stuffed_ds = new_ds

    return stuffed_ds


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


def n_dimensional_n_split(min_max_array, n, initializing_object = None):
    tiny_ds = pixel_blur_d(min_max_array, n)

    dimensions =  len(min_max_array)/2

    tiny_ds_per_big_d = len(tiny_ds)/dimensions

    from rtree import index

    p = index.Property()
    p.dimension = dimensions

    idx = index.Index(properties=p, interleaved=True)

    for i in xrange(tiny_ds_per_big_d):
        pt = [tiny_ds[i*dimensions +x] for x in range(dimensions)]
        pt = [pt[j//2] for j in range(len(pt)*2)]
        idx.insert(i, tuple(pt), obj=initializing_object)

    while tiny_ds_per_big_d < n:
        r = n - tiny_ds_per_big_d

        more_pts = pixel_blur_d(min_max_array, r)
        for index in xrange(len(more_pts) / dimensions):
            pt = [more_pts[index * dimensions + x] for x in range(dimensions)]
            pt.extend(pt)
            if len(list(idx.intersection(tuple(pt), objects=True)))==0:
                idx.insert(tiny_ds_per_big_d+index,
                           tuple(pt),
                           obj=initializing_object)
            else:
                neighbors = list(idx.nearest(tuple(pt), 2, objects=True))
                n1 = neighbors[0].bbox
                n2 = neighbors[1].bbox
                new_pt = []
                for a in xrange(len(n1)):
                    new_pt.append(int((n1[a]+n2[a])/2))
                idx.insert(tiny_ds_per_big_d+index,
                           tuple(new_pt),
                           obj=initializing_object)
        tiny_ds_per_big_d = tiny_ds_per_big_d + len(more_pts)/dimensions

    return idx

def n_dimensional_n_split_float(min_max_array, n, initializing_object=None):
    tiny_ds = pixel_blur_d_float(min_max_array, n)

    dimensions =  len(min_max_array)/2

    tiny_ds_per_big_d = len(tiny_ds)/dimensions

    from rtree import index

    p = index.Property()
    p.dimension = dimensions
    #p.interleaved=True

    idx = index.Index(properties=p, interleaved=True)

    for i in xrange(tiny_ds_per_big_d):
        pt = [tiny_ds[i*dimensions +x] for x in range(dimensions)]
        idx.insert(i, tuple(pt), obj=initializing_object)

    while tiny_ds_per_big_d < n:
        r = n - tiny_ds_per_big_d

        more_pts = pixel_blur_d_float(min_max_array, r)
        for index in xrange(len(more_pts) / dimensions):
            pt = [more_pts[index * dimensions + x] for x in range(dimensions)]
            if len(list(idx.intersection(tuple(pt), objects=True)))==0:
                idx.insert(tiny_ds_per_big_d+index,
                           tuple(pt),
                           obj=initializing_object)
            else:
                neighbors = list(idx.nearest(tuple(pt), 2, objects=True))
                n1 = neighbors[0].bbox
                n2 = neighbors[1].bbox
                new_pt = []
                for a in xrange(len(n1)):
                    new_pt.append((n1[a]+n2[a])/2.0)
                idx.insert(tiny_ds_per_big_d+index,
                           tuple(new_pt),
                           obj=initializing_object)
        tiny_ds_per_big_d = tiny_ds_per_big_d + len(more_pts)/dimensions

    return idx

if __name__ == "__main__":

    field = n_dimensional_n_split_float([-27, 37, 0, 500,0,8, 0, 2], 10000)
    points = list(field.intersection((-27, 0,0, 0, 37, 500, 8, 2), objects=True))
    print([(point.id, point.bbox) for point in points])
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

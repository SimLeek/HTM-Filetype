import math

def XORShiftRNG(seed):
    r=seed
    r ^= (r<<21)
    r ^= (r>>35)
    r ^= (r<<4)
    return r

def randInt(min_val, max_val, seed):
    #naive rand int. needs replacing
    if (max_val-min_val)==0:
        return max_val
    return (XORShiftRNG(seed) % (max_val-min_val)) + min_val

def rand_split(a,b,seed):
    if a+1 >= b:
        raise IndexError("indices cannot be separated")
    #return randInt(a+1,b-1,seed)
    return int((a+b)/2)

def tree_split(a,b,depth,seed):
    vals=[a,b]

    for i in xrange(depth):
        l = len(vals) - 1
        for j in xrange(l):
            try:
                vals.append(rand_split(vals[j],vals[j+1],seed+i+j))
            except(IndexError):
                pass
        vals.sort()

    return vals

def n_split_points(min,max,n):
    step = int((max-min)/(n+1))

    vals=[]

    for i in xrange(1,n+1):
        vals.append(min+i*step)

    return vals

def n_split_points_float(min,max,n):
    step = (max-min)/(n+1)

    vals=[]

    for i in xrange(1,n+1):
        vals.append(min+i*step)

    return vals

def get_tiny_d_tip(lengths, i, n_cube_len):
    big_d_length = lengths[i]
    the_tip = big_d_length % n_cube_len

    return the_tip

def stuff_the_ds(min_max_array, lengths, n_cube_len):
    # n-dimensional space filling algorithm
    points = []
    for i in xrange(len(lengths)):
        offset = int((n_cube_len + get_tiny_d_tip(lengths, i, n_cube_len))/2)
        new_points = []
        if i==0:
            for j in xrange((lengths[i]) / (n_cube_len)):
                new_points.append(offset + min_max_array[i * 2] + n_cube_len * j)
        else:
            for j in xrange(len(points)/i):
                for k in xrange((lengths[i]) / (n_cube_len)):
                    for l in xrange(i):
                        new_points.append(points[j * i + l])
                    new_points.append(offset + min_max_array[i * 2] + n_cube_len * k)
        points = new_points

    return points

def stuff_the_ds_float(min_max_array, lengths, n_cube_len):
    # n-dimensional space filling algorithm
    points = []
    for i in xrange(len(lengths)):
        offset = (n_cube_len + get_tiny_d_tip(lengths, i, n_cube_len))/2
        new_points = []
        if i==0:
            for j in xrange(int((lengths[i]) / (n_cube_len))):
                new_points.append(offset + min_max_array[i * 2] + n_cube_len * j)
        else:
            for j in xrange(len(points)/i):
                for k in xrange(int((lengths[i]) / (n_cube_len))):
                    for l in xrange(i):
                        new_points.append(points[j * i + l])
                    new_points.append(offset + min_max_array[i * 2] + n_cube_len * k)
        points = new_points

    return points

def get_d_lengths(min_max_array):
    lengths = []

    for i in xrange(len(min_max_array)/2):
        lengths.append(min_max_array[i*2+1]-min_max_array[i*2])

    return lengths

def get_d_thickness(lengths):
    vol = 1
    for i in xrange(len(lengths)):
        vol = vol * lengths[i]
    return vol

def pixel_blur_d_float(min_max_array, n):
    if len(min_max_array)%2 != 0 or len(min_max_array)==0:
        raise IndexError("array is not correct size")

    lengths = get_d_lengths(min_max_array)

    thickness = get_d_thickness(lengths)

    tiny_d_cube_len = (thickness/n)**(1.0/(len(lengths)))

    return stuff_the_ds_float(min_max_array, lengths, tiny_d_cube_len)

def pixel_blur_d(min_max_array, n):
    if len(min_max_array)%2 != 0 or len(min_max_array)==0:
        raise IndexError("array is not correct size")

    lengths = get_d_lengths(min_max_array)

    thickness = get_d_thickness(lengths)

    tiny_d_cube_len = int(math.ceil((thickness/n)**(1.0/(len(lengths)))))

    return stuff_the_ds(min_max_array, lengths, tiny_d_cube_len)

def unknown_length_sorted_array_2n_search_1(search_val, arr, pos, array_div = 1):
    step = 1
    prev_pos = pos
    prev_val = None
    for i in xrange(array_div):
        try:
            if arr[pos*array_div + i] > search_val[i] and pos*array_div + i >= 0:
                while arr[pos*array_div + i] > search_val[i] and pos*array_div + i >= 0 \
                        and (i==0 or arr[pos * array_div + i - 1] == search_val[i - 1]):
                    prev_pos = pos
                    pos = pos - step
                    step = step*2
            elif arr[pos*array_div + i] < search_val[i] and pos*array_div + i >= 0:
                while arr[pos*array_div + i] < search_val[i] and pos*array_div + i >= 0\
                        and (i==0 or arr[pos*array_div + i - 1] == search_val[i-1]):
                    prev_pos = pos
                    pos = pos + step
                    step = step*2
            if arr[pos*array_div + i] != search_val[i]:
                break
            else:
                step = 1
        except IndexError:
            pass

    if pos < 0:
        pos = 0

    if (pos + 1)*array_div - 1 >= len(arr):
        pos = len(arr)/array_div - 1

    return prev_pos, pos

def order(a , b):
    if a > b:
        return b, a
    else:
        return a, b

def search_array_2n_contiguous_subset_axis_rightmost(search_val, arr, start, end, skip, axis):
    mid = int((end - start) / 2) + start

    while start != mid and mid != end:
        array_val = arr[mid * skip + axis]
        diff = 0
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
        diff = 0
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

    if search_val < arr[mid*skip + axis]:
        return mid - 1, False
    return mid, False

def search_array_2n_contiguous_subset(search_arr, arr, a, b):
    start, end = order(a,b)
    mid = int((end - start)/2) + start
    skip = len(search_arr)

    for i in xrange(len(search_arr)):
        if i!= len(search_arr)-1:
            start = search_array_2n_contiguous_subset_axis_leftmost(search_arr[i], arr, start, end, skip, i)
            end = search_array_2n_contiguous_subset_axis_rightmost(search_arr[i], arr, start, end, skip, i)
            if start == end:
                return (start - 1), False
        else:
            return search_array_2n_contiguous_subset_axis_first_match(search_arr[i], arr, start, end, skip, i)

def n_dimensional_midpoint(point1, point2):
    midpoint = []

    for i in xrange(len(point1)):
        dist = abs(point1[i] - point2[i])
        min_pt = min(point1[i], point2[i])
        midpoint.append(int(min_pt + dist / 2.0))

    return midpoint

def n_dimensional_n_split(min_max_array, n):

    tiny_ds = pixel_blur_d(min_max_array, n)

    dimensions = (len(min_max_array)/2)

    tiny_ds_per_big_d=len(tiny_ds) / dimensions


    while tiny_ds_per_big_d<n:
        n = n-tiny_ds_per_big_d

        more_pts = pixel_blur_d(min_max_array, n)
        for i in xrange(len(more_pts)/dimensions):
            pt = []
            for j in xrange(dimensions):
                pt.append(more_pts[i*dimensions+j])
            duplicate_loc, found = search_array_2n_contiguous_subset(pt, tiny_ds, 0, tiny_ds_per_big_d)

            if not found:
                new_tiny_ds = tiny_ds[0:duplicate_loc*n+n-1]
                new_tiny_ds.extend(pt)
                new_tiny_ds.extend(tiny_ds[duplicate_loc*n+n:-1])
                tiny_ds = new_tiny_ds
            else:
                if duplicate_loc!=tiny_ds_per_big_d:
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

    dimensions = (len(min_max_array)/2)

    tiny_ds_per_big_d=len(tiny_ds) / dimensions


    while tiny_ds_per_big_d<n:
        n = n-tiny_ds_per_big_d

        more_pts = pixel_blur_d_float(min_max_array, n)
        for i in xrange(len(more_pts)/dimensions):
            pt = []
            for j in xrange(dimensions):
                pt.append(more_pts[i*dimensions+j])
            duplicate_loc, found = search_array_2n_contiguous_subset(pt, tiny_ds, 0, tiny_ds_per_big_d)

            if not found:
                new_tiny_ds = tiny_ds[0:duplicate_loc*n+n-1]
                new_tiny_ds.extend(pt)
                new_tiny_ds.extend(tiny_ds[duplicate_loc*n+n:-1])
                tiny_ds = new_tiny_ds
            else:
                if duplicate_loc!=tiny_ds_per_big_d:
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
    maximum=9223372036854775807
    minimum=0


    test_array = []
    for i in xrange(100):
        test_array.append(randInt(0,10000,48736489723+i))

    test_array.sort()


    test_array = n_dimensional_n_split([0,100,0,100], 100)


    print("test_array:", test_array)

    a , b = unknown_length_sorted_array_2n_search_1([65,95], test_array, 50, 2)
    print("alg:", a , b)
    print("arr a:", test_array[2*a], test_array[2*a+1])
    print("arr b:", test_array[2 * b], test_array[2 * b + 1])

    #loc = search_array_2n_contiguous_subset([65,85], test_array, 0, 100)
    split = n_dimensional_n_split_float([0,100,0,100], 137)

    print(split)



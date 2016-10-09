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

def get_tiny_d_tip(min_max_array, i, n_cube_len):
    big_d_length = min_max_array[i+1] - min_max_array[i]
    ds_overflowing = math.ceil(big_d_length / float(n_cube_len))
    the_tip = ds_overflowing * n_cube_len - big_d_length

    return the_tip

def stuff_the_ds(min_max_array, lengths, n_cube_len):
    # n-dimensional space filling algorithm
    points = []
    for i in xrange(len(min_max_array) / 2):
        offset = int(get_tiny_d_tip(min_max_array, i, n_cube_len) / 2.0)
        new_points = []
        for j in xrange((lengths[i]) / (n_cube_len)):
            for k in xrange(i):
                new_points.append(points[k])
            new_points.append(-offset + min_max_array[i * 2] + n_cube_len * j)
        points = new_points

    return points

def get_d_lengths(min_max_array):
    lengths = {}

    for i in xrange(len(min_max_array), step=2):
        if min_max_array[i+1]-min_max_array[0] not in lengths:
            lengths[min_max_array[i+1]-min_max_array[0]]=[]
        lengths[min_max_array[i + 1] - min_max_array[0]].append(i)

    return lengths

def get_d_thickness(lengths):
    vol = 1
    for i in xrange(len(lengths)):
        vol = vol * lengths[i]
    return vol

def pixel_blur_d(min_max_array, n):
    if len(min_max_array)%2 != 0 or len(min_max_array)==0:
        raise IndexError("array is not correct size")

    lengths = get_d_lengths(min_max_array)

    thickness = get_d_thickness(lengths)

    tiny_d_cube_len = int(math.ceil((thickness**(1.0/(len(lengths)))) / n))

    return stuff_the_ds(min_max_array, lengths, tiny_d_cube_len)



if __name__ == "__main__":
    max=9223372036854775807
    min=0

    print(n_split_points(min,max, 100))

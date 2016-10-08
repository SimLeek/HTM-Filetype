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

def all_the_ds(min_max_array, lengths, n_cube_len):
    # n-dimensional space filling algorithm
    points = []
    for i in xrange(len(min_max_array) / 2):
        new_points = []
        for j in xrange((lengths[i]) / (n_cube_len)):
            for k in xrange(i):
                new_points.append(points[k])
            new_points.append(min_max_array[i * 2] + n_cube_len * j)
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

def n_dimensional_n_split(min_max_array, n):
    if len(min_max_array)%2 != 0 or len(min_max_array)==0:
        raise IndexError("array is not correct size")

    lengths = get_d_lengths(min_max_array)

    thickness = get_d_thickness(lengths)

    tiny_d_cube_len = int(((thickness**(1.0/(len(lengths)))) / n)+.5)

    tiny_ds = all_the_ds(min_max_array, lengths, tiny_d_cube_len)

    tiny_ds_per_big_d=len(tiny_ds) / (len(min_max_array)/2)

    sorted_d_lengths = sorted(lengths)

    if tiny_ds_per_big_d<n:
        #select one of the dimensions, remove, and use the
        # n-dimensional space filling algorithm
        #to fill it up with as many points as it can hold,
        #then, add the max or min to the points in the original removed dimension place
        #add points to point array until num==n, going out from center projected onto largest face
        #if num!=n still, add points to next largest face

    elif tiny_ds_per_big_d>n:
        #remove points closest to smallest faces, going inwards, until num==n



if __name__ == "__main__":
    max=9223372036854775807
    min=0

    print(n_split_points(min,max, 100))

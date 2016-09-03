import random
import time
import math

def XORShiftRNG(seed):
    r=seed
    r ^= (r<<21)
    r ^= (r>>35)
    r ^= (r<<4)
    return r

def randInt(min_val, max_val, seed):
    #naive rand int. needs replacing
    return (XORShiftRNG(seed) % max_val-min_val) + min_val

def binaryTreeGetParent(index):
    if index == 0:
        return None
    else:
        return math.floor((index-1)/2)

def binaryTreeGetLeftSibling(index):
    if index == 2**math.floor(math.log(index+1,2))-1:
        return None
    else:
        return index-1

def binaryTreeGetRightSibling(index):
    if index+1 == 2**math.floor(math.log(index+2,2)-1):
        return None
    else:
        return index+1

def randomBucketSizeArray(size_min, size_max, num_buckets, seed):
    #todo: generate a log_2 access only version of this
    array=[]
    array.append(randInt(size_min+1,size_max-1, seed))

    for i in range(1,num_buckets):
        parent = binaryTreeGetParent(i)
        if i%2==1:
            min_divider = binaryTreeGetLeftSibling(parent)
            if min_divider == None:
                min_divider = size_min+1
            else:
                min_divider = array[min_divider]+1
            max_divider = array[parent]-1
        else:
            max_divider = binaryTreeGetRightSibling(parent)
            if max_divider == None:
                max_divider = size_max-1
            else:
                max_divider = array[max_divider]-1
            min_divider = array[parent]+1
        if max_divider - min_divider <0:
                num_buckets=num_buckets+1
                continue
        array.append(randInt(min_divider, max_divider, seed+i))

    array.append(size_min)
    array.append(size_max)

    array.sort()

    return array

def randomOfArray(array, min_loc, max_loc, seed):
    return array[randInt(min_loc, max_loc, seed)]

def randomSample(array, size, seed):
    #not true random sample. Divides array into buckets and selects from each.
    # should be good enough, and should be much faster.

    if size>len(array):
        raise IndexError("Desired output array size is larger than input size")

    #todo: check type and other things

    subset= []

    buckets = randomBucketSizeArray(0, size, seed)

    for i in xrange(size):
        index = randInt(buckets[i], buckets[i+1]-1, seed+i)
        subset.append(array[index])

    #not needed for HTM
    #random.shuffle(subset)

    return subset

#def randomSampleAt(index, array, size, seed):
#    bucket_size=len(array)/size
#    i = randInt(index*bucket_size, (i+1)*bucket_size-1, seed)
#    return array[i]

#def randomSampleSubset()

if __name__ == "__main__":
    arr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

    random.seed(time.time())

    sub = randomSample(xrange(1000000000),1000000)

    print(sub)

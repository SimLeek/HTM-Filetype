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
    if (max_val-min_val)==0:
        return max_val
    return (XORShiftRNG(seed) % (max_val-min_val)) + min_val

'''def binaryTreeGetParent(index):
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
        return index+1'''

def randomOfArray(array, min_loc, max_loc, seed):
    return array[randInt(min_loc, max_loc, seed)]

def randomSample(input_array, size, seed):
    #Algorithm R implementation
    sample = []

    for i in range(size):
        sample.append(input_array[i])

    for i in range(size, len(input_array)):
        r = randInt(0,i-1, seed + i)

        if r < size:
            sample[r] = input_array[i]

    return sample

if __name__ == "__main__":
    arr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

    random.seed(time.time())

    sub = randomSample(xrange(10000),1000, 574386534)

    print(sub)

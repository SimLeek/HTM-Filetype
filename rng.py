import numbers

def xor_shift_rng(seed):
    r = seed
    assert isinstance(r, numbers.Integral)
    r ^= (r << 21)
    r ^= (r >> 35)
    r ^= (r << 4)
    return r


def rand_int(min_val, max_val, seed):
    # naive rand int. needs replacing
    if (max_val - min_val) == 0:
        return max_val
    return (xor_shift_rng(seed) % (max_val - min_val)) + min_val

from rtree import index

p = index.Property()
p.dimension = 5

idx = index.Index(properties=p)

if __name__ == "__main__":

    from rand_bin_subset import n_dimensional_n_split

    # need to make this so much faster...
    split = n_dimensional_n_split([0,1920,0,1080,0,255,0,255,0,255], 10000)

    for i in xrange(len(split)/5):
        idx.insert(i,(split[i*5],split[i*5+1],split[i*5+2],split[i*5+3],split[i*5+4],
                      split[i * 5], split[i * 5 + 1], split[i * 5 + 2], split[i * 5 + 3], split[i * 5 + 4]))

    print(list(idx.intersection((0,0,0,0,0,200,200,255,255,255) )))

    print(list(idx.nearest((500, 500, 255, 255, 255, 500, 500, 255, 255, 255), 20)))
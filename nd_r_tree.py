from rtree import index

p = index.Property()
p.dimension = 5

idx = index.Index(properties=p)

if __name__ == "__main__":

    from n_d_point_field import n_dimensional_n_split

    # need to make this so much faster...
    split = n_dimensional_n_split([0,1920,0,1080,0,255,0,255,0,255], 10000)

    for i in xrange(len(split)/5):
        idx.insert(i,(split[i*5],split[i*5+1],split[i*5+2],split[i*5+3],split[i*5+4],
                      split[i * 5], split[i * 5 + 1], split[i * 5 + 2], split[i * 5 + 3], split[i * 5 + 4]),
                   obj = i)

    points = ((idx.intersection((0,0,0,0,0,200,200,255,255,255), objects=True )))

    print([(point.id, point.bbox) for point in points])

    #works for finding nearby points to interpolate between in the case of extra points
    points = (list(idx.nearest((500, 500, 255, 255, 255, 500, 500, 255, 255, 255), 20, objects=True)))

    print([(point.id, point.bbox) for point in points])

    #works for finding points at exact location
    points = (list(idx.intersection((69, 54, 127, 208, 208, 69, 54, 127, 208, 208), objects=True)))

    print([(point.id, point.bbox) for point in points])

    #works for using n_dimensional array for rtree insertion/removal
    a = [500, 500, 255, 255, 255, 500, 500, 255, 255, 255]
    a_mod = tuple(a)

    print(a)
    print(a_mod)
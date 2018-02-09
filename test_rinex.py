
'''
(c) 2017 Oleksandr Bogomaz

Tests of RINEX files parsing.
'''

import gnss.rinex as rinex
import gnss.coord as coord


if __name__ == '__main__':

    r = rinex.read_obs('./data/BASE307L.17O')
    header = r['header']
    print(coord.geo(**header.get_pos()))
    print(header.get_num_of_obs(), header.get_types_of_obs())
    data = r['data']
    print(len(data))
    print(data[0])

    sat = set()
    for d in data:
        for s in d['sat']:
            sat.add(s)
    sat = list(sat)
    sat.sort()
    print(sat)

    for d in data:
        params = d['param']
        for k, p in params.items():
            if k == "G01":
                print(p[0], p[4], sep='\t')

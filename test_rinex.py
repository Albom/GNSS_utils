
'''
(c) 2017 Oleksandr Bogomaz

Tests of RINEX files parsing.
'''

import gnss.rinex as rinex
import gnss.coord as coord


r = rinex.read_obs('./data/BASE307L.17O')
header = r['header']
print(coord.geo(**header.get_pos()))
print(header.get_num_of_obs(), header.get_types_of_obs())
data = r['data']
print(len(data))
print(data[0])

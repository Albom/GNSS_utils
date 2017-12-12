
'''
(c) 2017 Oleksandr Bogomaz

Tests of RINEX files parsing.
'''

import gnss.rinex as rinex
import gnss.coord as coord


r = rinex.read_obs('./data/BASE307L.17O')
print(coord.geo(**r['header'].get_pos()))

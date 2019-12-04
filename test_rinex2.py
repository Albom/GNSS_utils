
'''
(c) 2017 Oleksandr Bogomaz

Tests of RINEX 2 files parsing.
'''

import gnss.rinex2 as rinex2
import gnss.coord as coord

if __name__ == '__main__':

    r = rinex2.read_obs('./data/BASE0180.19O')
    header = r['header']
    print('Approximate coordinates: ', coord.geo(**header.get_pos()))
    print(header.get_num_of_obs(), header.get_types_of_obs())
    data = r['data']
    print(len(data), ' records in file')
    g01 = filter(lambda x: 'G01' in x['sat'], data)
    print('G01 data moments: ', [x['date'].isoformat() for x in g01])

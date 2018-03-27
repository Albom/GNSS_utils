
'''
(c) 2017 Oleksandr Bogomaz

Tests of coordinates converting.
'''

import gnss.coord as coord

if __name__ == '__main__':

    d1 = {'x': 3411557.3382, 'y': 2348463.8352, 'z': 4834396.6426}
    d2 = d1
    for i in range(0, 1000):
        g1 = coord.geo(**d2)
        d2 = coord.xyz(**g1)
    print(d1['x']-d2['x'], d1['y']-d2['y'], d1['z']-d2['z'], sep='\n')

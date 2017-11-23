
'''
(c) 2017 Oleksandr Bogomaz

Tests of coordinates converting.
'''

import gnss.coord as coord

print(coord.geo(x=3411557.3382, y=2348463.8352, z=4834396.6426))
print(coord.xyz(lat=67.251508, long=26.232056,  height=299.7))

print(coord.geo(**coord.xyz(lat=67.251508, long=26.232056,  height=299.7)))

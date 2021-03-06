
'''
(c) 2017 Oleksandr Bogomaz
Based on the code written by Glenn D. MacGougan (GDM),
http://gnsstk.sourceforge.net

Utilities for coordinates converting.
'''

import math


class WGS_84:
    A = 6378137.0
    B = 6356752.31414
    E2 = (A ** 2 - B ** 2) / A ** 2


ELLIPSE = WGS_84


def xyz(**kwargs):
    rad = math.pi / 180.0
    lat = kwargs['lat'] * rad
    long = kwargs['long'] * rad
    height = kwargs['height']
    n = ELLIPSE.A / math.sqrt(1.0 - ELLIPSE.E2 * math.sin(lat) ** 2.0)
    x = (n + height) * math.cos(lat) * math.cos(long)
    y = (n + height) * math.cos(lat) * math.sin(long)
    z = ((1.0 - ELLIPSE.E2) * n + height) * math.sin(lat)
    return {'x': x, 'y': y, 'z': z}


def geo(**kwargs):
    x = kwargs['x']
    y = kwargs['y']
    z = kwargs['z']
    eps = 1.0e-15
    if (math.fabs(x) < eps) & (math.fabs(y) < eps):
        lat = math.copysign(math.pi / 2, z)
        long = 0.0
        height = math.fabs(z) - ELLIPSE.B
    else:
        p = math.hypot(x, y)
        long = 2.0 * math.atan2(y, x + p)
        lat = math.atan(z / (p * (1.0 - ELLIPSE.E2)))
        height = 0.0
        while True:
            prev = height
            n = ELLIPSE.A / math.sqrt(1 - ELLIPSE.E2 * math.sin(lat) ** 2)
            height = p / math.cos(lat) - n
            lat = math.atan(z / (p * (1 - ELLIPSE.E2 * n / (n + height))))
            if math.fabs(height - prev) < eps:
                break

        deg = 180.0 / math.pi
        return {'lat': lat * deg, 'long': long * deg, 'height': height}

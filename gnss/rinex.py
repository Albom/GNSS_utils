
'''
(c) 2017 Oleksandr Bogomaz

RINEX files parsing.
'''

from gnss.header import Header as Header


def read_obs(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    header = Header()
    i = 0
    while True:
        line = lines[i]
        description = line[60:-1].strip()
        if description == Header.END_OF_HEADER:
            break
        elif description == Header.RINEX_VERSION_TYPE:
            header.set_version(line[:9].strip())
            header.set_type(line[20:21])
            if header.get_type() != 'O':
                return {}
        elif description == Header.APPROX_POSITION_XYZ:
            d = 14
            header.set_pos({'x': float(line[:d]),
                            'y': float(line[d:2*d]),
                            'z': float(line[2*d:3*d])})
        i += 1

    return {'header': header}

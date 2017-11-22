
'''
(c) 2017 Oleksandr Bogomaz

RINEX files parsing.
'''


class Header:
    RINEX_VERSION_TYPE = 'RINEX VERSION / TYPE'
    PGM_RUN_BY_DATE = 'PGM / RUN BY / DATE'
    COMMENT = 'COMMENT'
    MARKER_NAME = 'MARKER NAME'
    MARKER_NUMBER = 'MARKER NUMBER'
    OBSERVER_AGENCY = 'OBSERVER / AGENCY'
    REC_TYPE_VERS = 'REC # / TYPE / VERS'
    ANT_TYPE = 'ANT # / TYPE'
    APPROX_POSITION_XYZ = 'APPROX POSITION XYZ'
    ANTENNA_DELTA_H_E_N = 'ANTENNA: DELTA H/E/N'
    WAVELENGTH_FACT_L1_2 = 'WAVELENGTH FACT L1/2'
    TYPES_OF_OBSERV = '# / TYPES OF OBSERV'
    INTERVAL = 'INTERVAL'
    TIME_OF_FIRST_OBS = 'TIME OF FIRST OBS'
    TIME_OF_LAST_OBS = 'TIME OF LAST OBS'
    LEAP_SECONDS = 'LEAP SECONDS'
    END_OF_HEADER = 'END OF HEADER'
    _version = ''

    def getVersion(self):
        return self._version

    def setVersion(self, version):
        self._version = version


def read_obs(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    header = Header()
    i = 0
    while True:
        line = lines[i]
        description = line[60:-1].strip()
        print(description)
        if description == Header.END_OF_HEADER:
            break
        elif description == Header.RINEX_VERSION_TYPE:
            header.setVersion(line[:9].strip())
        i += 1

    print(header.getVersion())
    return

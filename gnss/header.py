
'''
(c) 2017 Oleksandr Bogomaz

RINEX header.
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
    _type = ''
    _pos = {'x': 0, 'y': 0, 'z': 0}

    def get_version(self):
        return self._version

    def set_version(self, version):
        self._version = version

    def get_type(self):
        return self._type

    def set_type(self, _type):
        self._type = _type

    def get_pos(self):
        return self._pos

    def set_pos(self, _pos):
        self._pos = _pos

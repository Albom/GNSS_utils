
'''
(c) 2017-2019 Oleksandr Bogomaz

RINEX 2 header.
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
    __version = ''
    __type = ''
    __pos = {'x': 0, 'y': 0, 'z': 0}
    __num_of_obs = 0
    __types_of_obs = []

    def get_version(self):
        return self.__version

    def set_version(self, version):
        self.__version = version

    def get_type(self):
        return self.__type

    def set_type(self, __type):
        self.__type = __type

    def get_pos(self):
        return self.__pos

    def set_pos(self, __pos):
        self.__pos = __pos

    def get_num_of_obs(self):
        return self.__num_of_obs

    def set_num_of_obs(self, num_of_obs):
        self.__num_of_obs = num_of_obs

    def get_types_of_obs(self):
        return self.__types_of_obs

    def add_types_of_obs(self, types):
        self.__types_of_obs.append(types)

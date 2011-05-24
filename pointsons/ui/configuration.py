from ..configuration import Configuration

from .area import Area

class UIConfiguration(Configuration):    
    def __init__(self, aPSUI):
        Configuration.__init__(self, '/dev/null')

        self.area = Area(aPSUI)



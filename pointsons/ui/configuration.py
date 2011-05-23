from ..configuration import Configuration

from ..area import Area

from ..osc import ServerParameter

class UIArea(Area, ServerParameter):
    def __init__(self, aPSUI):
        self.psui = aPSUI
        
    def on_x_changed(self):
        x_adj = self.psui.builder.get_object('area_x_adj')
        x_adj.set_value(self.x)
        self.to_server()
        
    def on_z_changed(self):
        z_adj = self.psui.builder.get_object('area_z_adj')
        z_adj.set_value(self.z)
        self.to_server()

    def on_radius_changed(self):
        radius_adj = self.psui.builder.get_object('area_radius_adj')
        radius_adj.set_value(self.radius)
        self.to_server()

    def to_server(self):
        self._osc_to_server('/pointsons/area',
                            self.x,
                            self.z,
                            self.radius)
        

class UIConfiguration(Configuration):    
    def __init__(self, aPSUI):
        Configuration.__init__(self, '/dev/null')

        self.area = UIArea(aPSUI)



from ..area import AbstractArea
from ..osc import ServerParameter

class Area(AbstractArea, ServerParameter):
    """
    Area on ther UI side : sends its config to the server
    """
    def __init__(self, aPSUI):
        self.psui = aPSUI

        AbstractArea.__init__(self)
        ServerParameter.__init__(self)
        
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





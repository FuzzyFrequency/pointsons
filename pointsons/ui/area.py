from ..area import AbstractArea

class Area(AsbtractArea):
    def on_x_changed(self):
        self.to_server()

    def on_z_changed(self):
        self.to_server()

    def on_radius_changed(self):
        self.to_server()




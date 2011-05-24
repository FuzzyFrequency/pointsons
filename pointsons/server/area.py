from ..area import AbstractArea
from .kinect import KinectParameter

class Area(AbstractArea, KinectParameter):
    def on_x_changed(self):
        self.to_kinect()

    def on_z_changed(self):
        self.to_kinect()

    def on_radius_changed(self):
        self.to_kinect()

    def to_kinect(self):
        return self._osc_to_kinect('/area',
                                   self.x,
                                   self.z,
                                   self.radius
                                   )




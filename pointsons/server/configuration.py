from mididings.units import Filter
from mididings import NOTEON, Scene

from ..configuration import Configuration

from .osc import PointSonsOSCInterface

class ServerConfiguration(Configuration):
    def setup_kinect(self):
        """
        Send the initialization sequence to the kinect system
        """
        # Global parameters
        self.to_kinect()

        # Camera
        self.camera.to_kinect()

        # Area
        self.area.to_kinect()

    def to_scene(self):
        return {
            1: Filter(NOTEON)
            }

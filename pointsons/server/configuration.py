from mididings.units import Filter
from mididings import NOTEON, Scene

from ..configuration import Configuration

from .kinect import KinectParameter
from .osc import PointSonsOSCInterface

class ServerConfiguration(Configuration, KinectParameter):
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

        # FIXME: Need a way to delete all bowls

        from .bowl import Bowl
        from ..note import Note
        b = Bowl()
        b.position = (10, 20, 30)
        b.radius = 10
        n = Note()
        n.label = "c#2"
        b.note = n
        
        self.bowls = [b]

        # Bowls
        for bowl in self.bowls:
            bowl.to_kinect()

    def to_scene(self):
        return {
            1: Filter(NOTEON)
            }

    def to_kinect(self):
        self._osc_to_kinect('/config',
                            self.ratioEyeBodySize,
                            self.ratioCylinderRayFromShouldersSpace,
                            self.proximityCenterForHeadCalculation,
                            self.armBlobNumbermin,
                            self.croppingXMin,
                            self.croppingXMax,
                            self.croppingYMin,
                            self.croppingYMax,
                            self.lowPassFilter,
                            self.eyeDepthOffset,
                            self.bodyDepthOffset,
                            self.armSquaredDistanceThreshold,
                            self.ratioArmLengthFromHeight,
                            self.ratioHeightWidthMin,
                            self.userProfile
                            )


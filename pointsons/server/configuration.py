from ..configuration import Configuration
from ..constants import KINECT_OSC_CONFIG, KINECT_OSC_CAMERA, KINECT_OSC_AREA
from .osc import PointSonsOSCInterface, send_to_kinect

class ServerConfiguration(Configuration):
    def setup_kinect(self):
        """
        Send the initialization sequence to the kinect system
        """

        # Global setup
        send_to_kinect(KINECT_OSC_CONFIG,
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

        # Camera
        send_to_kinect(KINECT_OSC_CAMERA,
                       self.camera.position[0],
                       self.camera.position[1],
                       self.camera.position[2],
                       self.camera.orientation)

        # Area
        send_to_kinect(KINECT_OSC_AREA,
                       self.area.x,
                       self.area.z,
                       self.area.radius)

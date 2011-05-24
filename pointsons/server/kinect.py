import liblo

import settings

class KinectParameter(object):
    def _osc_to_kinect(self, path, *arguments):
        """
        Send an OSC message to the kinect software
        The path is a tuple, made of :
        (osc_path, osc_format)
        Paths can be found in constants.py.
        """
        print "Sending OSC:", path, arguments
        liblo.send(settings.KINECT_OSC_PORT,
                   path,
                   *arguments)

    def to_kinect(self):
        """
        Objects should implement this method to send their data to the
        kinect
        """
        raise NotImplemented()


    

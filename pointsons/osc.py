import liblo

import settings

class ServerParameter(object):
    def _osc_to_server(self, path, *arguments):
        """
        Send an OSC message to the kinect software
        The path is a tuple, made of :
        (osc_path, osc_format)
        Paths can be found in constants.py.
        """
        liblo.send(settings.SERVER_OSC_PORT,
                   path,
                   *arguments)

    def to_server(self):
        pass

    def to_ui(self):
        pass
    
    

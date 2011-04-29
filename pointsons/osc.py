from mididings.extra.osc import OSCInterface
from liblo import make_method

class PointSonsOSCInterface(OSCInterface):
    @make_method('/pointsons/sphere', 'f')
    def sphere(self, path, probability):
        print "got sphere", path, probability

    @make_method('/pointsons/gesture', 'f')
    def gesture(self, path, probability):
        print "got gesture", path, probability







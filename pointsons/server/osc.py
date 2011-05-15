import mididings.engine as engine
from mididings.extra.osc import OSCInterface
from mididings.event import NoteOnEvent, NoteOffEvent
from mididings.util import note_number
from liblo import make_method

class PointSonsOSCInterface(OSCInterface):
    @make_method('/pointsons/sphere', 'f')
    def sphere(self, path, probability):
        print "got sphere", path, probability
        engine._TheEngine().process(NoteOnEvent(engine.in_ports()[0], 1, note_number('C2'), 100))

    @make_method('/pointsons/gesture', 'f')
    def gesture(self, path, probability):
        print "got gesture", path, probability







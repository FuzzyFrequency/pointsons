# -*- coding: utf-8 -*-
#
# Pointsons
#
# Copyright (C) 2011 Guillaume Libersat <guillaume@fuzzyfrequency.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#

import mididings.engine as engine
from mididings.extra.osc import OSCInterface
from mididings.event import NoteOnEvent, NoteOffEvent
from mididings.util import note_number
import liblo
from liblo import make_method

import settings

class PointSonsOSCInterface(OSCInterface):
    @make_method('/pointsons/sphere', 'f')
    def sphere(self, path, probability):
        print "got sphere", path, probability
        engine._TheEngine().process(NoteOnEvent(engine.in_ports()[0], 1, note_number('C2'), 100))

    @make_method('/pointsons/gesture', 'f')
    def gesture(self, path, probability):
        print "got gesture", path, probability

def send_to_kinect(path, *arguments):
    """
    Send an OSC message to the kinect software
    The path is a tuple, made of :
    (osc_path, osc_format)
    Paths can be found in constants.py.
    """
    liblo.send(settings.KINECT_OSC_PORT,
               path[0],
               path[1],
               *arguments)
    




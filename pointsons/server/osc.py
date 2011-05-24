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
    #-- From UI Side
    @make_method('/pointsons/area', 'iii')
    def area(self, path, args):
        print "area", args[0], args[1], args[2]

    @make_method('/pointsons/bowl/add', 'siiiii')
    def bowl_add(self, path, args):
        print "add bowl", args[0]

    @make_method('/pointsons/bowl/del', 's')
    def bowl_del(self, path, args):
        print "del bowl", args[0]


    #-- From Kinect Side
    @make_method('/test', 'si')
    def the_test(self, path, args):
        print "test", path, args

    @make_method('/probability/sphere', 'siff')
    def sphere(self, path, args):
        """
        0 -> Main droite
        1 -> Main Gauche
        """
        print "got sphere : %s '%s', %d, %f, %f" % (path, args[0], args[1], args[2], args[3])
        # engine._TheEngine().process(NoteOnEvent(engine.in_ports()[0], 1, note_number('C2'), 100))

    @make_method('/probability/gesture', 'sff')
    def gesture(self, path, args):
        print "got gesture", path, args[0]

    @make_method('/sphere/stop', 'sf')
    def sphere_stop(self, path, args):
        print "stop sphere", args[0]






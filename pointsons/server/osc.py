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

from ..configuration import Configurations

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
    @make_method('/kinect_reset', '')
    def kinect_reset(self, path, args):
        configs = Configurations()
        configs.current.setup_kinect()

    @make_method('/test', 'si')
    def the_test(self, path, args):
        print "test", path, args

    @make_method('/probability/sphere', 'siff')
    def sphere(self, path, args):
        """
        0 -> Main droite
        1 -> Main Gauche
        """
        note_name = args[0]
        hands = args[1]
        probability = args[2]
        force = args[3]
        if probability > 0.5:
            print "got sphere : %s '%s', %d, %f, %f" % (path, 
                                                        note_name, 
                                                        hands, 
                                                        probability,
                                                        force)
        
            engine._TheEngine().process(NoteOnEvent(engine.in_ports()[0], 1, note_number(note_name), 127))

    @make_method('/probability/gesture', 'sifffff')
    def one_hand_gesture(self, path, args):
        print "got one hand gesture", path, args

    @make_method('/probability/gesture', 'siffffffffff')
    def two_hands_gesture(self, path, args):
        print "got two hands gesture", path, args

    @make_method('/sphere/stop', 'sf')
    def sphere_stop(self, path, args):
        print "stop sphere", args[0]

    @make_method('/stopall', '')
    def stopall(self, path, args):
        print "stopall"

    @make_method('/pointing/rh', 'sf')
    def right_hand_pointing(self, path, args):
        note_name = args[0]
        p = args[1]
        print "in !", args
        if p < 1:
            engine._TheEngine().process(NoteOffEvent(engine.in_ports()[0], 1, note_number(note_name), 127))
        else:
            engine._TheEngine().process(NoteOnEvent(engine.in_ports()[0], 1, note_number(note_name), 127))
        # print "right hand pointing", path, args

    @make_method('/pointing/lh', 'sf')
    def left_hand_pointing(self, path, args):
        print "left hand pointing", path, args

    @make_method('/activeuser', 'i')
    def activeuser(self, path, args):
        print "active user", args


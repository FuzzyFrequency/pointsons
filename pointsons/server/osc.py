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
from mididings.event import CtrlEvent, PitchbendEvent
from mididings.util import note_number
import liblo
from liblo import make_method

import settings

from .scenes import context

from ..configuration import Configurations

class PointSonsOSCInterface(OSCInterface):
    def __init__(self, *args, **kwargs):
        OSCInterface.__init__(self, *args, **kwargs)

        self.configs = Configurations()
    
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

    @make_method('/probability/gesture', 'sfffff')
    def one_hand_gesture(self, path, args):
        name = args[0]
        if name == 'throwR':
            print "Got THROWR"
            engine._TheEngine().process(CtrlEvent(engine.in_ports()[0],
                                                  settings.MIDI_HAMMER_CHANNEL, 
                                                  1, # modwheel
                                                  int(args[2]), # value
                                                  )
                                        )
        else:
            print "Got Unknown Gesture"
                                            
    @make_method('/probability/gesture', 'sffffffffff')
    def two_hands_gesture(self, path, args):
        name = args[0]
        if name == 'chord':
            # proba, force, position (R, L)
            print "Got Chord"
            engine._TheEngine().process(PitchbendEvent(engine.in_ports()[0],
                                                       1,
                                                       1)
                                        )
        print "got two hands gesture", path, args

    @make_method('/sphere/stop', 'sf')
    def sphere_stop(self, path, args):
        sphere_name = args[0]
        print "stop sphere", sphere_name

        note = None
        for bowl in self.configs.current.bowls:
            if bowl.note.label == sphere_name:
                note = bowl.note.label
                break

        if note:
            engine._TheEngine().process(NoteOnEvent(engine.in_ports()[0],
                                                    settings.MIDI_DAMPER_CHANNEL,
                                                    note,
                                                    127)
                                        )
            print "sent stop", args


    @make_method('/stopall', '')
    def stopall(self, path, args):
        engine._TheEngine().process(CtrlEvent(engine.in_ports()[0],
                                              settings.MIDI_DAMPER_CHANNEL,
                                              123,
                                              0)
                                    )

    @make_method('/pointing/rh', 'sf')
    def right_hand_pointing(self, path, args):
        note_name = args[0]
        p = args[1]
        print "in !", args

    @make_method('/pointing/lh', 'sf')
    def left_hand_pointing(self, path, args):
        print "left hand pointing", path, args

    @make_method('/activeuser', 'i')
    def activeuser(self, path, args):
        user_active = args[0]

        if not user_active:
            context['tonality'] = None
            


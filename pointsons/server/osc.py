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
import math
        
import mididings.engine as engine

from mididings.extra.osc import OSCInterface
from mididings.event import NoteOnEvent, NoteOffEvent
from mididings.event import CtrlEvent, PitchbendEvent, AftertouchEvent
from mididings.util import note_number
from mididings import engine
from mididings import AFTERTOUCH
from liblo import make_method

import settings
from ..configuration import Configurations
from ..constants import *
from .scenes import context


class PointSonsOSCInterface(OSCInterface):
    def __init__(self, *args, **kwargs):
        OSCInterface.__init__(self, *args, **kwargs)

        self.configs = Configurations()


    @make_method('/quit', '')
    def quit_now(self, path, args):
        engine.quit()
    
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
        
        print "got sphere : %s '%s', %d, %f, %f" % (path, 
                                                    note_name, 
                                                    hands, 
                                                    probability,
                                                    force)

        bowls = {'c2': (0, 127),
                 'd2': (0, 127)}

        speed_min = 0
        speed_max = 1

        try:
            bowl_lower = bowls[note_name][0]
            bowl_upper = bowls[note_name][1]
        except KeyError:
            bowl_lower = 0
            bowl_upper = 127

        bowl_range = bowl_upper - bowl_lower
        step = float(speed_max) / bowl_range

        print step, bowl_range
        
        midi_vel = int(min(math.ceil(bowl_lower + (float(force*force + 0.1) / step) + 5), 127))

        print midi_vel

        if hands == RIGHT_HAND:
            engine._TheEngine().process(NoteOnEvent(engine.in_ports()[0],
                                                    settings.MIDI_HAMMER_CHANNEL,
                                                    note_number(note_name),
                                                    midi_vel)
                                        )

        elif hands == LEFT_HAND:
            engine._TheEngine().process(NoteOnEvent(engine.in_ports()[0],
                                                    settings.MIDI_REPEAT_CHANNEL,
                                                    note_number(note_name),
                                                    midi_vel)
                                        )

    @make_method('/touch', 's')
    def touch(self, path, args):
        name = args[0]

        if name == "head":
            print "got head"
            engine._TheEngine().process(AftertouchEvent(engine.in_ports()[0],
                                                        settings.MIDI_HAMMER_CHANNEL,
                                                        127)
                                       )
            

    @make_method('/throw', 'isf')
    def throw(self, path, args):
        hand = args[0]
        name = args[1]
        force = args[2]

        right_hand_evmap = {'dlur': RH_GLIS_UP,
                            'urdl': RH_GLIS_DOWN,
                            'rl': WHOLE_ALTERED,
                            'lr': INSCALE_UP,
                            'drul': RH_RAF_UP,
                            'uldr': RH_RAF_DOWN
                            }

        left_hand_evmap = {'dlur': LH_GLIS_UP,
                           'urdl': LH_GLIS_DOWN,
                           'uldr': LH_RAF_DOWN,
                           'drul': LH_RAF_UP,
                           'lr': WHOLE_NORMAL,
                           'rl': INSCALE_DOWN,
                           }

        if hand == LEFT_HAND:
            midi_event = left_hand_evmap[name]
        elif hand == RIGHT_HAND:
            midi_event = right_hand_evmap[name]
        else:
            midi_event = -1
            print "PROBLEM !!"

        step = 1.0 / 127
        midi_vel = int(min(math.floor(float(force*0.75 + 0.001) / step), 127))
        
        print ">>>>> throwing", name, force, midi_vel
        
        engine._TheEngine().process(CtrlEvent(engine.in_ports()[0],
                                              settings.MIDI_HAMMER_CHANNEL, 
                                              midi_event, # modwheel
                                              midi_vel, # value
                                              )
                                    )

        

    @make_method('/probability/gesture', 'sfffff')
    def one_hand_gesture(self, path, args):
        name = args[0]
        if name == 'throwR':
            print "Got THROWR"
            engine._TheEngine().process(CtrlEvent(engine.in_ports()[0],
                                                  settings.MIDI_HAMMER_CHANNEL, 
                                                  LOWER_OCTAVE, # modwheel
                                                  int(args[2])+20, # value
                                                  )
                                        )
        else:
            print "Got Unknown Gesture"
                                            
    @make_method('/probability/gesture', 'sfffffff')
    def two_hands_gesture(self, path, args):
        """
        name, force, xyz_r, xyz_l
        """
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

    @make_method('/pointing/lh', 's')
    def left_hand_pointing(self, path, args):
        note = args[0]
        if note == "":
            note = "c2"
        engine._TheEngine().process(NoteOffEvent(engine.in_ports()[0],
                                                 settings.MIDI_REPEAT_CHANNEL,
                                                 note,
                                                 127)
                                    )
        
    @make_method('/activeuser', 'i')
    def activeuser(self, path, args):
        user_active = args[0]

        if not user_active:
            context['tonality'] = None
            


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
from threading import Timer, Lock
import copy
import math
import time

import mididings.engine as engine
from mididings import KeyFilter, Discard, Scene, Filter, Channel, Transpose, Process, Call, Pass
# Constants
from mididings import NOTEON, NOTEOFF, AFTERTOUCH, CTRL, PITCHBEND
# Filter
from mididings.units.filters import CtrlFilter, ChannelFilter
# Events
from mididings.event import NoteOnEvent, NoteOffEvent
from mididings.util import note_number
import mididings.misc as _misc

import settings
from ..constants import *

# Output routing
to_dampers = Channel(settings.MIDI_DAMPER_CHANNEL)
to_hammers = Channel(settings.MIDI_HAMMER_CHANNEL)


context_lock = Lock()
context = {'latest_note': 48,
           'history': [],
           'tonality': None,
           'mode': "major",
           'glissando_is_running': False,
           'chord_is_running': False,
           'history_is_running': False,
           'inhib_hits': False}

# Context modifiers
def update_latest_note(anEvent):
    if context['tonality'] == None:
        context['tonality'] = anEvent.note
    context['latest_note'] = anEvent.note

    return anEvent

def update_history(anEvent):
    if not context['history_is_running']:
        if len(context['history']) >= 10:
            context['history'].pop(0)
        
        context['history'].append((anEvent.note, anEvent.velocity, time.time()))
    
    return anEvent

# Inhib hits
def inhib_hits(anEvent):
    context['inhib_hits'] = True
    return anEvent

def desinhib_hits(anEvent=None):
    context['inhib_hits'] = False
    return anEvent

# Generators
def generate_chord(anEvent):
    if context['chord_is_running']:
        return
    
    context['chord_is_running'] = True

    tonic = context['latest_note']
    scale = ORIENTAL2_SCALE
    interval = ['third']


    _MODES = ['ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
    _INTERVALS = ['unison', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'octave',
                  'ninth', 'tenth', 'eleventh', 'twelfth', 'thirteenth']

    # Calculate chord based on tonality and scale (may need to add
    # mode parameter)
    print "chords = ",
    for shift in range(0, 3):
        print tonic+scale[shift*2],
        yield NoteOnEvent(anEvent.port,
                          anEvent.channel,
                          tonic+scale[shift*2],
                          127)
    print

    def reallow_chords():
        context['chord_is_running'] = False
    d = Timer(0.5, reallow_chords)

    # FIXME: Threads may need to be collected !
    d.start()

    
    

def generate_all_notes_on(anEvent):
    """
    Activate all bowls.
    Ding Generator.
    """
    for note in range(note_number(settings.BOWL_LOWER), 
                      note_number(settings.BOWL_UPPER)):
        yield NoteOnEvent(anEvent.port,
                          anEvent.channel,
                          note, 127)


generate_neighbours = [Transpose(-1), Transpose(1)]


# glissando
def schedule_glissando(ev):
    import random

    context_lock.acquire()
    is_running = context['glissando_is_running']
    context_lock.release()
    
    if is_running:
        print "glissando running, quit."
        return
    else: 
        context_lock.acquire()       
        context['glissando_is_running'] = True
        context_lock.release()


    # speed of glissando
    velocity = ev.value

    scale = ORIENTAL2_SCALE

    tonic = context['latest_note']

    print "tonic is", tonic
    if tonic >= note_number('c3') and ev.ctrl == GLIS_UP:
        tonic -= 12
    if tonic < note_number('c3') and ev.ctrl == GLIS_DOWN:
        tonic += 12
        
    note_range = range(tonic, note_number('c5'))


    # Scaleless
    total_lower_octave = range(note_number('c2'), note_number('c3'))
    total_upper_octave = range(note_number('c3'), note_number('c4'))
    total_whole_octave = total_lower_octave + total_lower_octave

    # In-scale
    scale_lower_octave = [total_lower_octave[offset] for offset in scale]
    scale_upper_octave = [total_upper_octave[offset] for offset in scale]
    scale_whole_octave = scale_lower_octave + scale_upper_octave
    
    scale_whole_octave_reversed = copy.copy(scale_whole_octave)
    scale_whole_octave_reversed.reverse()

    # Normal mask
    normal_mask = [0, 2, 4, 5, 7, 9, 11]
    altered_mask = [1, 3, 6, 8, 10]

    # Scaleless, normal
    total_lower_normal = [total_lower_octave[offset] for offset in normal_mask]
    total_upper_normal = [total_upper_octave[offset] for offset in normal_mask]
    total_whole_normal = total_lower_normal + total_upper_normal

    # Scaleless, altered
    total_lower_altered = [total_lower_octave[offset] for offset in altered_mask]
    total_upper_altered = [total_upper_octave[offset] for offset in altered_mask]
    total_whole_altered = total_lower_altered + total_upper_altered

    scale_up = [note_range[offset] for offset in scale]
    scale_down = copy.copy(scale_up)
    scale_down.reverse()

    
    #whole_altered = [note for note in note_range if not note in whole_normal]
    #lower_altered = whole_altered[:5]
    #upper_altered = whole_altered[5:]


    notes_to_play = {GLIS_UP: scale_up,
                     GLIS_DOWN: scale_down,
                     WHOLE_NORMAL: total_whole_normal,
                     #LOWER_ALTERED: lower_altered,
                     #UPPER_ALTERED: upper_altered,
                     WHOLE_ALTERED: total_whole_altered,
                     #LOWER_OCTAVE: lower_octave,
                     #UPPER_OCTAVE: upper_octave,
                     #WHOLE_OCTAVE: whole_octave,
                     INSCALE_UP: scale_whole_octave,
                     INSCALE_DOWN: scale_whole_octave_reversed,
                     }[ev.ctrl]

    print "glissando at", velocity, "for", notes_to_play
        
    def throw_glissando_note(note):
        for note in notes_to_play:
            try:
                engine._TheEngine().process(NoteOnEvent(engine.in_ports()[0], 
                                                        settings.MIDI_HAMMER_CHANNEL, 
                                                        note,
                                                        120)
                                            )
            except Exception, e:
                print "Failure during glissando"


            sleep_min = 0.012
            sleep_max = 0.216
            sleep_time = max(sleep_max - (math.log10(max(velocity, 1))  / 11.75), sleep_min)
            time.sleep(sleep_time)
            
        context_lock.acquire()
        print "glissand to false"
        context['glissando_is_running'] = False
        context_lock.release()


    d = Timer(0, throw_glissando_note, kwargs={'note': 127})

    # FIXME: Threads may need to be collected !
    d.start()


glissando = ChannelFilter(settings.MIDI_HAMMER_CHANNEL) >> CtrlFilter([1,2,3,4,5,6,7,8,9]) >> Process(schedule_glissando)


# History
def schedule_history(ev):
    """
    Start a thread, not handled by Dings, so that the events are sent
    before it ends.
    """
    if not context['history_is_running']:
        context['history_is_running'] = True
    else:
        return
    
    history = copy.copy(context['history'])

    print "scheduling history", history
    
    def play():
        for i, record in enumerate(history):
            engine._TheEngine().process(NoteOnEvent(engine.in_ports()[0], 
                                                     settings.MIDI_HAMMER_CHANNEL, 
                                                     record[0],
                                                     record[1])
                                    )

            # Wait until next note
            if i <= (len(history)-2):
                waiting = history[i+1][2] - record[2]
                
                time.sleep(waiting)

        context['history'] = []
        context['history_is_running'] = False

    d = Timer(0, play)

    # FIXME: Threads may need to be collected !
    d.start()



# Stop an area
def schedule_dampers_release(ev):
    """
    Start a thread, not handled by Dings, so that the events are sent
    before it ends.
    """
    def throw_damper_release_note(note):
        engine._TheEngine().process(NoteOffEvent(engine.in_ports()[0], 
                                                 settings.MIDI_DAMPER_CHANNEL, 
                                                 note, 
                                                 127)
                                    )
        

    d = Timer(3, throw_damper_release_note, kwargs={'note': ev.note})

    # FIXME: Threads may need to be collected !
    d.start()

def schedule_desinhib(ev):
    d = Timer(3, desinhib_hits)
    d.start()
    return ev

area_stop = [generate_neighbours, Pass()] >> Call(schedule_dampers_release) >> to_dampers

# Bowls
hammer_activate = ChannelFilter(settings.MIDI_HAMMER_CHANNEL) >> Process(update_latest_note) >> Process(update_history) >> to_hammers
damper_activate = ChannelFilter(settings.MIDI_DAMPER_CHANNEL) >> area_stop
damper_release = ChannelFilter(settings.MIDI_DAMPER_CHANNEL) >> to_dampers


# Stop all bowls. 123 = All Notes Off
stop_all = ChannelFilter(settings.MIDI_DAMPER_CHANNEL) >> CtrlFilter(123) >> Process(schedule_desinhib) >> Process(inhib_hits) >> Process(generate_all_notes_on) >> Call(schedule_dampers_release) >> to_dampers

# Chord
chord = Process(generate_chord) >> Process(update_history) >> to_hammers


noteon_router = hammer_activate // damper_activate
ctrl_router =  Filter(CTRL) >> (stop_all // glissando)

play_history = Process(schedule_history) >> Discard()

def inhib_if_necessary(anEvent):
    if context['inhib_hits'] and anEvent.channel == settings.MIDI_HAMMER_CHANNEL:
        print "!!!!!events inhibed!!!!!"
        return None
    else:
        return anEvent

# Main scene
public_router = Process(inhib_if_necessary) >> {
    NOTEON: noteon_router,
    NOTEOFF: damper_release,
    CTRL: ctrl_router,
    PITCHBEND: chord,
    AFTERTOUCH: play_history,
    }

xx = Pass()

ps_scenes = {
    1: Scene("Public", public_router),
    2: Scene("Artiste", []),
    3: Scene("Auto", [])
}







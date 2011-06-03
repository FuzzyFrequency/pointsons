from threading import Timer
import time
import math
import copy

# Constants
from mididings import NOTEON, NOTEOFF, AFTERTOUCH, CTRL, PITCHBEND
# Filter
from mididings import KeyFilter, Discard
from mididings.patch import Patch
# Units
from mididings.units.filters import CtrlFilter, ChannelFilter
from mididings.event import NoteOnEvent, NoteOffEvent
from mididings import Scene, Filter, Channel, Transpose, NoteOn, NoteOff, Process, Call, Generator, Pass
from mididings.util import _NOTE_NAMES, note_number
from mididings.extra.harmonizer import Harmonize, _Harmonizer

import mididings.engine as engine

from ..constants import *

import mididings.util

import settings

# Output routing
to_dampers = Channel(settings.MIDI_DAMPER_CHANNEL)
to_hammers = Channel(settings.MIDI_HAMMER_CHANNEL)

context = {'latest_note': 48,
           'history': [],
           'tonality': None,
           'mode': "major",
           'glissando_is_running': False,
           'chord_is_running': False,
           'history_is_running': False}

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

# Generators
def generate_chord(anEvent):
    if context['chord_is_running']:
        return
    
    context['chord_is_running'] = True

    import mididings.misc as _misc

    MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
    HARMONIC_MINOR_SCALE = [0, 2, 3, 5, 7, 8, 11]
    
    tonic = context['latest_note']
    scale = HARMONIC_MINOR_SCALE
    interval = ['third']


    _MODES = ['ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
    _INTERVALS = ['unison', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'octave',
                  'ninth', 'tenth', 'eleventh', 'twelfth', 'thirteenth']

    # Calculate chord based on tonality and scale (may need to add
    # mode parameter)
    for shift in range(0, 6, 2):
        yield NoteOnEvent(anEvent.port,
                          anEvent.channel,
                          tonic+scale[shift],
                          127)
                       

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
    
    if context['glissando_is_running']:
        return
    else:
        context['glissando_is_running'] = True


    # speed of glissando
    velocity = ev.value

    scale = [0, 2, 4, 5, 7, 9, 11]
    note_range = range(mididings.util.note_number('c2'), mididings.util.note_number('c4'))

    lower_normal = [note_range[offset] for offset in scale]
    upper_normal = [note_range[offset+12] for offset in scale]
    whole_normal = lower_normal + upper_normal

    whole_altered = [note for note in note_range if not note in whole_normal]
    lower_altered = whole_altered[:5]
    upper_altered = whole_altered[5:]

    lower_octave = note_range[:12]
    upper_octave = note_range[12:]
    whole_octave = lower_octave + upper_octave

    notes_to_play = {LOWER_NORMAL: lower_normal,
                     UPPER_NORMAL: upper_normal,
                     WHOLE_NORMAL: whole_normal,
                     LOWER_ALTERED: lower_altered,
                     UPPER_ALTERED: upper_altered,
                     WHOLE_ALTERED: whole_altered,
                     LOWER_OCTAVE: lower_octave,
                     UPPER_OCTAVE: upper_octave,
                     WHOLE_OCTAVE: whole_octave}[ev.ctrl]

    print "glissando at", velocity, "for", notes_to_play
        
    def throw_glissando_note(note):
        for note in notes_to_play:
            engine._TheEngine().process(NoteOnEvent(engine.in_ports()[0], 
                                                    settings.MIDI_HAMMER_CHANNEL, 
                                                    note, 
                                                    127)
                                        )


            sleep_min = 0.012
            sleep_max = 0.216
            sleep_time = max(sleep_max - (math.log10(max(velocity, 1))  / 9.75), sleep_min)
            time.sleep(sleep_time)
            
        context['glissando_is_running'] = False


    d = Timer(0, throw_glissando_note, kwargs={'note': 127})

    # FIXME: Threads may need to be collected !
    d.start()


glissando = ChannelFilter(settings.MIDI_HAMMER_CHANNEL) >> CtrlFilter([1,2,3,4,5,6]) >> Process(schedule_glissando)


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

area_stop = [generate_neighbours, Pass()] >> Call(schedule_dampers_release) >> to_dampers

# Bowls
hammer_activate = ChannelFilter(settings.MIDI_HAMMER_CHANNEL) >> Process(update_latest_note) >> Process(update_history) >> to_hammers
damper_activate = ChannelFilter(settings.MIDI_DAMPER_CHANNEL) >> area_stop
damper_release = ChannelFilter(settings.MIDI_DAMPER_CHANNEL) >> to_dampers


# Stop all bowls. 123 = All Notes Off
stop_all = ChannelFilter(settings.MIDI_DAMPER_CHANNEL) >> CtrlFilter(123) >> Process(generate_all_notes_on) >> Call(schedule_dampers_release) >> to_dampers

# Chord
chord = Process(generate_chord) >> Process(update_history) >> to_hammers


noteon_router = hammer_activate // damper_activate
ctrl_router =  Filter(CTRL) >> (stop_all // glissando)

play_history = Process(schedule_history) >> Discard()

# Main scene
public_router = {
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







from threading import Timer
import time

# Constants
from mididings import NOTEON, NOTEOFF, POLY_AFTERTOUCH, CTRL, PITCHBEND
# Filter
from mididings import KeyFilter
from mididings.patch import Patch
# Units
from mididings.units.filters import CtrlFilter, ChannelFilter
from mididings.event import NoteOnEvent, NoteOffEvent
from mididings import Scene, Filter, Channel, Transpose, NoteOn, NoteOff, Process, Call, Generator, Pass
from mididings.util import _NOTE_NAMES, note_number
from mididings.extra.harmonizer import Harmonize, _Harmonizer

import mididings.engine as engine

import mididings.util

import settings

# Output rrouting
to_dampers = Channel(settings.MIDI_DAMPER_CHANNEL)
to_hammers = Channel(settings.MIDI_HAMMER_CHANNEL)

context = {'latest_note': 'c2'}

# Context modifiers
def update_latest_note(anEvent):
    context['latest_note'] = anEvent.note
    return anEvent

# Generators
def generate_chord(anEvent):
    import mididings.misc as _misc

    tonic = context['latest_note'].rstrip('0123456789')
    scale = _MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
    interval = ['third']

    _HARMONIC_MINOR_SCALE = [0, 2, 3, 5, 7, 8, 11]
    _MODES = ['ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
    _INTERVALS = ['unison', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'octave',
                  'ninth', 'tenth', 'eleventh', 'twelfth', 'thirteenth']


    t = mididings.util.tonic_note_number(tonic)

    if _misc.issequence(scale):
        shift = 0
    elif isinstance(scale, str):
        if scale == 'major':
            scale = _MAJOR_SCALE
            shift = 0
        elif scale == 'minor':
            scale = _MAJOR_SCALE
            shift = 5
        elif scale == 'minor_harmonic':
            scale = _HARMONIC_MINOR_SCALE
            shift = 0
        elif scale in _MODES:
            shift = _MODES.index(scale)
            scale = _MAJOR_SCALE

    # shift scale to the correct mode
    s = [x - scale[shift] for x in scale[shift:]] + \
        [x + 12 - scale[shift] for x in scale[:shift]]

    if not _misc.issequence(interval):
        interval = [interval]

    # convert all interval names to numbers
    iv = [(_INTERVALS.index(x) if x in _INTERVALS else x) for x in interval]

    # python version:
    # f = [ Process(_Harmonizer(t, s, i, non_harmonic)) for i in iv ]

    harmo = [ _Harmonizer(t, s, i, 'below')(NoteOnEvent(anEvent.port,
                                                        settings.MIDI_HAMMER_CHANNEL,
                                                        context['latest_note'],
                                                        127))
              for i in iv 
              ]

    print harmo
    
    

def generate_all_notes_on(anEvent):
    for note in range(note_number(settings.BOWL_LOWER), 
                      note_number(settings.BOWL_UPPER)):
        yield NoteOnEvent(anEvent.port,
                          anEvent.channel,
                          note, 127)


generate_neighbours = [Transpose(-1), Transpose(1)]

# Stop an area
def schedule_dampers_release(ev):
    def throw_damper_release_note(anEvent):
        engine._TheEngine().process(NoteOffEvent(engine.in_ports()[0], 
                                                 settings.MIDI_DAMPER_CHANNEL, 
                                                 anEvent.note, 
                                                 127)
                                    )  

    d = Timer(2, throw_damper_release_note, kwargs={'anEvent': ev})

    # FIXME: Threads may need to be collected !
    d.start()

area_stop = [generate_neighbours, Pass()] >> Call(schedule_dampers_release) >> to_dampers

# Bowls
hammer_activate = ChannelFilter(settings.MIDI_HAMMER_CHANNEL) >> Process(update_latest_note) >> to_hammers
damper_activate = ChannelFilter(settings.MIDI_DAMPER_CHANNEL) >> area_stop
damper_release = ChannelFilter(settings.MIDI_DAMPER_CHANNEL) >> to_dampers


# Stop all bowls. 123 = All Notes Off
stop_all = CtrlFilter(123) >> Process(generate_all_notes_on) >> Call(schedule_dampers_release) >> to_dampers

# Chord
chord = Process(generate_chord) >> to_hammers



noteon_router = hammer_activate // damper_activate

# Main scene
public_router = {
    NOTEON: noteon_router,
    NOTEOFF: damper_release,
    CTRL: stop_all,
    PITCHBEND: chord,
    }

ps_scenes = {
    1: Scene("Public", public_router),
    2: Scene("Artiste", []),
    3: Scene("Auto", [])
}







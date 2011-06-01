from threading import Timer
import time

# Constants
from mididings import NOTEON, NOTEOFF, POLY_AFTERTOUCH, CTRL, PITCHBEND
# Filter
from mididings import KeyFilter
# Units
from mididings.units.filters import CtrlFilter, ChannelFilter
from mididings.event import NoteOnEvent, NoteOffEvent
from mididings import Scene, Filter, Channel, Transpose, NoteOn, NoteOff, Process, Call, Generator, Pass
from mididings.util import _NOTE_NAMES, note_number
from mididings.extra import Harmonize

import mididings.engine as engine

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
    for i in Harmonize(context['latest_note'], 'minor', ['third', 'fifth']):
        yield i

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







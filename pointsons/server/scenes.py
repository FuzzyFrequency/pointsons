from mididings import Scene, Channel, NOTEON, Filter, Transpose, NoteOn
from mididings.extra import Harmonize

public_scene = Filter(NOTEON) >> (NoteOn('d2', 127)
                                  // NoteOn('f2', 127)) >> Harmonize('c#', 'aeolian', 'octave') >> Channel(1)

ps_scenes = {
    1: Scene("Public", public_scene),
    2: Scene("Artiste", []),
    3: Scene("Auto", [])
}







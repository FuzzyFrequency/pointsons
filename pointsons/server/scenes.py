from mididings import Scene, Channel, NOTE, Filter, Transpose
from mididings.extra import Harmonize

public_scene = Filter(NOTE) >> Transpose(12) >> Harmonize('c#', 'minor_harmonic', ['unison', 'third', 'fifth']) >> Channel(1)

ps_scenes = {
    1: Scene("Public", public_scene),
    2: Scene("Artiste", []),
    3: Scene("Auto", [])
}







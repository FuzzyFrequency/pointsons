#!/usr/bin/env python

from mididings import hook, run
from mididings import Filter, PROGRAM, Print
from mididings.extra import MemorizeScene
from mididings.extra.inotify import AutoRestart

import settings
from pointsons.osc import PointSonsOSCInterface
from pointsons.scenes import ps_scenes
from pointsons.control import ps_control

if settings.DEBUG:
    pre = Print('input', portnames='in') >> ~Filter(PROGRAM)
    post = Print('output', portnames='out')
else:
    pre = post = None

hook(
    PointSonsOSCInterface(),
    MemorizeScene('scene.txt'),
    AutoRestart(),
)

run(scenes=ps_scenes,
    control=ps_control,
    pre=pre,
    post=post)



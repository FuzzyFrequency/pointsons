#!/usr/bin/env python

from mididings import hook, run
from mididings import Filter, PROGRAM, Print
from mididings.extra.inotify import AutoRestart

import settings
from pointsons.server.memorize import MemorizeConfig
from pointsons.server.osc import PointSonsOSCInterface
from pointsons.server.scenes import ps_scenes
from pointsons.server.control import ps_control

if settings.DEBUG:
    pre = Print('input', portnames='in') >> ~Filter(PROGRAM)
    post = Print('output', portnames='out')
else:
    pre = post = None

hook(
    PointSonsOSCInterface(port=settings.SERVER_OSC_PORT,
                          notify_ports=[settings.KINECT_OSC_PORT,
                                        settings.UI_OSC_PORT]),
    MemorizeConfig('config.ps'),
    AutoRestart(),
)

run(scenes=ps_scenes,
    control=ps_control,
    pre=pre,
    post=post)

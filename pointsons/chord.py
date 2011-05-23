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

from mididings.units import NoteOn

class Hit(object):
    bowl = None
    velocity = 127

    def to_patch(self):
        return NoteOn(bowl.note, self.veloticy)

class Chord(object):
    """
    A chord is composed of multiple bowls
    """
    trigged_bowls = []

    def to_patch(self):
        all_hits = ()
        
        for hit in trigged_bowls:
            all_hits = all_hits // hit.to_patch()

        return all_hits

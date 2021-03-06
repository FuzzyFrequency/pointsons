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

from ..gesture import AbstractGesture
from .kinect import KinectParameter

class Gesture(AbstractGesture, KinectParameter):
    def to_kinect(self):
        self._osc_to_kinect('/gesture',
                            self.name,
                            self.hands,
                            self.direction[0],
                            self.direction[1],
                            self.direction[2]
                            )






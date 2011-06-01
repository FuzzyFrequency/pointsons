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

from ..camera import AbstractCamera
from .kinect import KinectParameter

class Camera(AbstractCamera, KinectParameter):
    def to_kinect(self):
        self._osc_to_kinect('/camera',
                            self.position[0],
                            self.position[1],
                            self.position[2],
                            self.angle)




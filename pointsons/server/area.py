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
from ..area import AbstractArea
from .kinect import KinectParameter

class Area(AbstractArea, KinectParameter):
    def on_x_changed(self):
        self.to_kinect()

    def on_z_changed(self):
        self.to_kinect()

    def on_radius_changed(self):
        self.to_kinect()

    def to_kinect(self):
        return self._osc_to_kinect('/area',
                                   self.x,
                                   self.z,
                                   self.radius
                                   )




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

from mididings.units import Filter
from mididings import NOTEON, Scene

from ..configuration import Configuration

from .kinect import KinectParameter
from .osc import PointSonsOSCInterface

class ServerConfiguration(Configuration, KinectParameter):
    def setup_kinect(self):
        """
        Send the initialization sequence to the kinect system
        """
        # Global parameters
        self.to_kinect()

        # Camera
        self.camera.to_kinect()

        # # FIXME: Need a way to delete all bowls

        # from .bowl import Bowl
        # from ..note import Note
        # b = Bowl()
        # b.position = (0, 1000, 0)
        # b.radius = 500
        # n = Note()
        # n.label = "c#2"
        # b.note = n
        
        # self.bowls = [b]

        # Bowls
        for bowl in self.bowls:
            bowl.to_kinect()

        # Gestures
        for gesture in self.gestures:
            gesture.to_kinect()

        # Area
        self.area.to_kinect()


    def to_scene(self):
        return {
            1: Filter(NOTEON)
            }

    def to_kinect(self):
        self._osc_to_kinect('/config',
                            self.ratioEyeBodySize,
                            self.ratioCylinderRayFromShouldersSpace,
                            self.proximityCenterForHeadCalculation,
                            self.armBlobNumbermin,
                            self.croppingXMin,
                            self.croppingXMax,
                            self.croppingYMin,
                            self.croppingYMax,
                            self.lowPassFilter,
                            self.eyeDepthOffset,
                            self.bodyDepthOffset,
                            self.armSquaredDistanceThreshold,
                            self.ratioArmLengthFromHeight,
                            self.ratioHeightWidthMin,
                            self.userProfile
                            )

        self._osc_to_kinect('/minproba',
                            self.minProba)

                            

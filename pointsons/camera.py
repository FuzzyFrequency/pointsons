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
from .kinect import KinectParameter

class Camera(KinectParameter):
    """
    La caméra doit absolument être configurée dès le départ du
    programme. Sa configuration nécessite 4 paramètres :

     - 3 entiers en mm pour sa position dans l'espace(par rapport au
    point de référence choisi pour tout configurer);

     - 1 entier en degrés pour son orientation (de -27 si elle regarde
    vers le haut à 27 si elle regarde vers le bas).
    """
    position = (0, 0, 0) # (x, y, y) : mm, from reference point
    orientation = 0 # from -27 (looking at the sky) to +27 (looking at the floor)

    def to_kinect(self):
        self._osc_to_kinect('/camera',
                            self.position[0],
                            self.position[1],
                            self.position[2],
                            self.orientation)

        

        

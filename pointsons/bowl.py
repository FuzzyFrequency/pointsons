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

from .utils import Observable

class AbstractBowl(Observable):
    """
    Un bol est décrit par les éléments suivants :
    
     - un nom (une chaîne de caractère) ;
     
     - la main à observer (0 : main droite , 1 : main gauche , 2 : les
       deux mains) ;

     - une position dans l'espace (toujours 3 entiers en mm par
       rapport au même point de référence) ;
     
     - un rayon (en mm).
    """
    note = None
    position = (0, 0, 0) # mm, from reference point
    radius = 0 # mm
    hands = 2 # Both hands


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

class AbstractArea(Observable):
    """
    Si il n'y a pas de zone dans lequel l'utilisateur peut interagir
    avec l'œuvre alors il n'y aura jamais d'interactions. Une zone est
    décrite par sa position dans l'espace et son rayon.
    """
    x = 0 # mm
    z = 0 # mm
    radius = 0 # mm

    

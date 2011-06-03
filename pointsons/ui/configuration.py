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
from ..configuration import Configuration

from .area import Area

class UIConfiguration(Configuration):    
    def __init__(self, aPSUI):
        Configuration.__init__(self, '/dev/null')

        self.area = Area(aPSUI)



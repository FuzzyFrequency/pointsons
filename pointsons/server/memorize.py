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

import mididings.setup as _setup
import mididings.engine as _engine

from configuration import ServerConfiguration

import sys as _sys

class MemorizeConfig(object):
    def __init__(self, config_path):
        self.config_path = config_path
        
    def on_start(self):
        try:
            self.configuration = ServerConfiguration.load(self.config_path)
        except IOError:
            # couldn't open configuration file, start with a fresh config
            self.configuration = ServerConfiguration(self.config_path)

        # Reconfigure the Kinect with the previous state
        self.configuration.setup_kinect()

    def on_exit(self):
        self.configuration.save()
            

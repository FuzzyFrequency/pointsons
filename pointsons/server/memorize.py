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
from ..configuration import Configurations
from .configuration import ServerConfiguration

class MemorizeConfig(object):
    def __init__(self, config_path):
        self.config_path = config_path

        self.configs = Configurations()

    def test_bowls(self):
        for bowl in self.configs.current.bowls:
            bowl.trigger()

    def on_start(self):
        try:
            configuration = ServerConfiguration.load(self.config_path)
        except IOError:
            # couldn't open configuration file, start with a fresh config
            configuration = ServerConfiguration(self.config_path)

        self.configs.set_current(configuration)

        # # Reconfigure the Kinect with the previous state
        self.configs.current.setup_kinect()

        # # Test bowls
        # self.test_bowls()

        # Build scenes from configuration and set them
        scene = self.configs.current.to_scene()

    def on_exit(self):
        self.configs.current.save()
            

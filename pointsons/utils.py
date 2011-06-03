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

class Borg:
    """
    The Borg or Monostate pattern
    """
    __shared_state = {}
    def __init__(self):
         self.__dict__ = self.__shared_state


class Observable(object):
    def __setattr__(self, field_name, aValue):
        """
        On value change, calls a callback named after the field name.
        """
        object.__setattr__(self, field_name, aValue)
        if hasattr(self, "on_%s_changed" % field_name):
            callback = getattr(self, "on_%s_changed" % field_name)
            callback()



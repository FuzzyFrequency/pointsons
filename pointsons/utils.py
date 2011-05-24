class Borg:
    """
    The Borg or Monostate pattern
    """
    __shared_state = {}
    def __init__(self):
         self.__dict__ = self.__shared_state


class Observable:
    def __setattr__(self, field_name, aValue):
        """
        On value change, calls a callback named after the field name.
        """
        object.__setattr__(self, field_name, aValue)
        if hasattr(self, "on_%s_changed" % field_name):
            callback = getattr(self, "on_%s_changed" % field_name)
            callback()



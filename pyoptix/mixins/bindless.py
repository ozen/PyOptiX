class BindlessMixin(object):
    def __init__(self):
        self._bindless = False

    @property
    def bindless(self):
        return self._bindless

    @bindless.setter
    def bindless(self, value):
        value = bool(value)
        self._safe_native.auto_destroy = not value
        self._bindless = value

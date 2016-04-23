class OptixObject(object):
    _context = None
    _native = None
    _parents = None

    def __init__(self, context, native):
        self._context = context
        self._native = native
        self._parents = []

    @property
    def context(self):
        return self._context

    @property
    def native(self):
        return self._native

    def _add_parent(self, parent):
        self._parents.append(parent)

    def _remove_parent(self, parent):
        self._parents.remove(parent)

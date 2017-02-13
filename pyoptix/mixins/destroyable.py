class DestroyableObject(object):
    def __init__(self, native):
        self._native = native

    @property
    def _safe_native(self):
        if not self._native.is_destroyed:
            return self._native
        else:
            raise RuntimeError('Underlying OptiX object was destroyed before.')

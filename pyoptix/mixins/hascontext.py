import weakref


class HasContextMixin(object):
    def __init__(self, context):
        self._context_ref = weakref.ref(context)

    @property
    def _safe_context(self):
        ctx = self._context_ref()
        if ctx is not None:
            return ctx
        else:
            raise RuntimeError('Context of this object is no longer valid')

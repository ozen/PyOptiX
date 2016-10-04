class GraphNodeMixin(object):
    def __init__(self):
        self._parents = []

    def _add_parent(self, parent):
        self._parents.append(parent)

    def _remove_parent(self, parent):
        self._parents.remove(parent)

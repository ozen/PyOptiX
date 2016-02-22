class OptixHasChild(object):
    def __init__(self, allowed_children):
        self._children = []
        self._allowed_children = allowed_children

    def add_child(self, child):
        is_allowed = False

        for allowed_children in self._allowed_children:
            if isinstance(child, allowed_children):
                is_allowed = True
                break

        if not is_allowed:
            raise TypeError(
                "You can not add {0} to {1} as a child".format(child.__class__.__name__, self.__class__.__name__))

        total_child_count = self.get_child_count()
        self._set_child_count(total_child_count + 1)

        try:
            self._set_optix_child(total_child_count, child)
        except Exception as e:
            total_child_count = self.get_child_count()
            self._set_child_count(total_child_count - 1)
            raise e

        child._add_parent(self)
        self._children.append(child)
        return total_child_count

    def _set_optix_child(self, index, child):
        from pyoptix.objects.optix_acceleration import OptixAcceleration
        from pyoptix.objects.optix_geometry import OptixGeometry
        from pyoptix.objects.optix_geometry_group import OptixGeometryGroup
        from pyoptix.objects.optix_geometry_instance import OptixGeometryInstance
        from pyoptix.objects.optix_group import OptixGroup
        from pyoptix.objects.optix_material import OptixMaterial
        from pyoptix.objects.optix_selector import OptixSelector
        from pyoptix.objects.optix_transform import OptixTransform

        if isinstance(child, OptixAcceleration):
            self._set_child_acceleration(index, child)
        elif isinstance(child, OptixTransform):
            self._set_child_transform(index, child)
        elif isinstance(child, OptixGeometryGroup):
            self._set_child_geometry_group(index, child)
        elif isinstance(child, OptixSelector):
            self._set_child_selector(index, child)
        elif isinstance(child, OptixGroup):
            self._set_child_group(index, child)
        elif isinstance(child, OptixGeometryInstance):
            self._set_child_geometry_instance(index, child)
        elif isinstance(child, OptixGeometry):
            self._set_child_geometry(index, child)
        elif isinstance(child, OptixMaterial):
            self._set_child_material(index, child)
        else:
            raise TypeError(
                "You can not add {0} to {1} as a child".format(child.__class__.__name__, self.__class__.__name__))

    def remove_child(self, child):
        index = self._children.index(child)

        if index != len(self._children) - 1:
            # swap with the last child
            self._set_optix_child(index, self._children[-1])
            self._children[index], self._children[-1] = self._children[-1], self._children[index]

        self._remove_last_child()

    def _remove_last_child(self):
        self._children[-1]._remove_parent(self)
        self._remove_child(len(self._children)-1)
        self._children.pop()

    def get_children(self):
        return self._children

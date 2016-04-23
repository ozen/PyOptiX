class OptixParent(object):
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
        from pyoptix.objects.acceleration import AccelerationObj
        from pyoptix.objects.geometry import GeometryObj
        from pyoptix.objects.geometry_group import GeometryGroupObj
        from pyoptix.objects.geometry_instance import GeometryInstanceObj
        from pyoptix.objects.group import GroupObj
        from pyoptix.objects.material import MaterialObj
        from pyoptix.objects.selector import SelectorObj
        from pyoptix.objects.transform import TransformObj

        if isinstance(child, AccelerationObj):
            self._set_child_acceleration(index, child)
        elif isinstance(child, TransformObj):
            self._set_child_transform(index, child)
        elif isinstance(child, GeometryGroupObj):
            self._set_child_geometry_group(index, child)
        elif isinstance(child, SelectorObj):
            self._set_child_selector(index, child)
        elif isinstance(child, GroupObj):
            self._set_child_group(index, child)
        elif isinstance(child, GeometryInstanceObj):
            self._set_child_geometry_instance(index, child)
        elif isinstance(child, GeometryObj):
            self._set_child_geometry(index, child)
        elif isinstance(child, MaterialObj):
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

    def get_geometry_instances(self):
        geometry_instances = set()
        for child in self._children:
            geometry_instances = geometry_instances | set(child.get_geometry_instances())
        return list(geometry_instances)

    def get_materials(self):
        materials = set()
        for child in self._children:
            materials = materials | set(child.get_materials())
        return list(materials)

    def get_geometries(self):
        geometries = set()
        for child in self._children:
            geometries = geometries | set(child.get_geometries())
        return list(geometries)

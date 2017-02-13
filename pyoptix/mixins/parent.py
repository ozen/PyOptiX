class ParentMixin(object):
    def __init__(self, allowed_children, children=None):
        self._children = []
        self._allowed_children = allowed_children

        if children is not None:
            if not isinstance(children, list):
                raise TypeError('children parameter must be a list')

            for child in children:
                self.add_child(child)

    def add_child(self, child):
        if not any([isinstance(child, allowed) for allowed in self._allowed_children]):
            raise TypeError(
                "You can not add {0} to {1} as a child".format(child.__class__.__name__, self.__class__.__name__))

        total_child_count = self._safe_native.get_child_count()
        self._safe_native.set_child_count(total_child_count + 1)

        try:
            self._set_optix_child(total_child_count, child)
        except Exception as e:
            total_child_count = self._safe_native.get_child_count()
            self._safe_native.set_child_count(total_child_count - 1)
            raise e

        child._add_parent(self)
        self._children.append(child)
        return total_child_count

    def _set_optix_child(self, index, child):
        from pyoptix.acceleration import Acceleration
        from pyoptix.geometry import Geometry
        from pyoptix.geometry_group import GeometryGroup
        from pyoptix.geometry_instance import GeometryInstance
        from pyoptix.group import Group
        from pyoptix.material import Material
        from pyoptix.selector import Selector
        from pyoptix.transform import Transform

        if isinstance(child, Acceleration):
            self._safe_native.set_child_acceleration(index, child._safe_native)
        elif isinstance(child, Transform):
            self._safe_native.set_child_transform(index, child._safe_native)
        elif isinstance(child, GeometryGroup):
            self._safe_native.set_child_geometry_group(index, child._safe_native)
        elif isinstance(child, Selector):
            self._safe_native.set_child_selector(index, child._safe_native)
        elif isinstance(child, Group):
            self._safe_native.set_child_group(index, child._safe_native)
        elif isinstance(child, GeometryInstance):
            self._safe_native.set_child_geometry_instance(index, child._safe_native)
        elif isinstance(child, Geometry):
            self._safe_native.set_child_geometry(index, child._safe_native)
        elif isinstance(child, Material):
            self._safe_native.set_child_material(index, child._safe_native)
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
        self._safe_native.remove_child(len(self._children)-1)
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

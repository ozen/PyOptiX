from pyoptix.objects.optix_acceleration import OptixAcceleration
from pyoptix.objects.optix_geometry import OptixGeometry
from pyoptix.objects.optix_geometry_group import OptixGeometryGroup
from pyoptix.objects.optix_geometry_instance import OptixGeometryInstance
from pyoptix.objects.optix_group import OptixGroup
from pyoptix.objects.optix_material import OptixMaterial
from pyoptix.objects.optix_selector import OptixSelector
from pyoptix.objects.optix_transform import OptixTransform


class OptixHasChild(object):

    def __init__(self, allowed_children):
        self._children = []
        self._allowed_children = allowed_children
        self._object_which_can_have_children = None

    def add_child(self, child):
        is_allowed = False

        for allowed_children in self._allowed_children:
            if isinstance(child, allowed_children):
                is_allowed = True
                break

        if not is_allowed:
            raise TypeError("You can not add " +
                            child.__class__.__name__ + " child" +
                            " to " +
                            self.__class__.__name__)

        total_child_count = self.get_child_count()
        self._set_child_count(total_child_count + 1)

        # add here to children
        if isinstance(child, OptixAcceleration):
            self._set_child_acceleration(total_child_count, child)
        elif isinstance(child, OptixTransform):
            self._set_child_transform(total_child_count, child)
        elif isinstance(child, OptixGeometryGroup):
            self._set_child_geometry_group(total_child_count, child)
        elif isinstance(child, OptixSelector):
            self._set_child_selector(total_child_count, child)
        elif isinstance(child, OptixGroup):
            self._set_child_group(total_child_count, child)
        elif isinstance(child, OptixGeometryInstance):
            self._set_child_geometry_instance(total_child_count, child)
        elif isinstance(child, OptixGeometry):
            self._set_child_geometry(total_child_count, child)
        elif isinstance(child, OptixMaterial):
            self._set_child_material(total_child_count, child)
        else:
            raise TypeError("You can not add " +
                            self.__class__.__name__ +
                            " to " +
                            child.__class__.__name__ + " child")

        child._add_parent(self)
        self._children.append(child)
        return total_child_count

    def remove_child(self, child):
        index = self._children.index(child)
        self._remove_child(index)
        self._children.remove(child)
        child._remove_parent(self)

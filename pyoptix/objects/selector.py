from pyoptix._driver import NativeSelectorWrapper
from pyoptix.objects.shared.optix_parent import OptixParent
from pyoptix.objects.shared.optix_object import OptixObject


class SelectorObj(NativeSelectorWrapper, OptixObject, OptixParent):
    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        NativeSelectorWrapper.__init__(self, native)

        from pyoptix.objects.geometry_group import GeometryGroupObj
        from pyoptix.objects.group import GroupObj
        from pyoptix.objects.transform import TransformObj

        allowed_children = [GeometryGroupObj, GroupObj, SelectorObj, TransformObj]
        OptixParent.__init__(self, allowed_children)

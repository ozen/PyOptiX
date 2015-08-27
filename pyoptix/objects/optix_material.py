from pyoptix._driver import _OptixMaterialWrapper
from pyoptix.objects.commons.optix_object import OptixObject


class OptixMaterial(_OptixMaterialWrapper, OptixObject):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixMaterialWrapper.__init__(self, native)

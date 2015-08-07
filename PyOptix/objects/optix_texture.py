from PyOptixCpp.Core import _OptixTextureSamplerWrapper
from PyOptix.objects.commons.optix_object import OptixObject


class OptixTexture(_OptixTextureSamplerWrapper, OptixObject):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixTextureSamplerWrapper.__init__(self, native)

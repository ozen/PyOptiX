from pyoptix._driver import NativeTextureSamplerWrapper, RTfiltermode
from pyoptix.objects.shared.optix_object import OptixObject
from pyoptix.types import convert_filtering_mode, convert_wrap_mode, convert_read_mode, convert_indexing_mode


class TextureSamplerObj(NativeTextureSamplerWrapper, OptixObject):
    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        NativeTextureSamplerWrapper.__init__(self, native)
        self.buffer = None
        self.filtering_mode_minification = None
        self.filtering_mode_magnification = None
        self.filtering_mode_mipmapping = None

    def set_buffer(self, texture_array_idx, mip_level, buffer):
        self.buffer = buffer
        self._set_buffer(texture_array_idx, mip_level, buffer)

    def get_buffer(self):
        return self.buffer

    def set_filtering_modes(self, minification=None, magnification=None, mipmapping=None):
        minification = convert_filtering_mode(minification)
        magnification = convert_filtering_mode(magnification)
        mipmapping = convert_filtering_mode(mipmapping)

        if minification is None:
            minification = RTfiltermode.RT_FILTER_NONE

        if magnification is None:
            magnification = RTfiltermode.RT_FILTER_NONE

        if mipmapping is None:
            mipmapping = RTfiltermode.RT_FILTER_NONE

        self.filtering_mode_minification = minification
        self.filtering_mode_magnification = magnification
        self.filtering_mode_mipmapping = mipmapping

        self._set_filtering_modes(minification, magnification, mipmapping)

    def get_filtering_modes(self):
        return self.filtering_mode_minification, self.filtering_mode_magnification, self.filtering_mode_mipmapping

    def set_wrap_mode(self, dim, mode):
        mode = convert_wrap_mode(mode)
        self._set_wrap_mode(dim, mode)

    def set_read_mode(self, mode):
        mode = convert_read_mode(mode)
        self._set_read_mode(mode)

    def set_indexing_mode(self, mode):
        mode = convert_indexing_mode(mode)
        self._set_indexing_mode(mode)

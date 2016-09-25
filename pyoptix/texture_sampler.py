from pyoptix._driver import NativeTextureSamplerWrapper, OPTIX_VERSION, RTfiltermode, RTfiltermode
from pyoptix.context import current_context
from pyoptix.types import convert_filtering_mode, convert_wrap_mode, convert_read_mode, convert_indexing_mode


class TextureSampler(NativeTextureSamplerWrapper):
    def __init__(self, buffer, wrap_mode=None, indexing_mode=None,
                 read_mode=None, filter_mode=None, max_anisotropy=1):
        self._context = current_context()
        native = self._context._create_texture_sampler()
        NativeTextureSamplerWrapper.__init__(self, native)

        self.buffer = None
        self.filtering_mode_minification = None
        self.filtering_mode_magnification = None
        self.filtering_mode_mipmapping = None

        if indexing_mode is not None:
            self.set_indexing_mode(indexing_mode)

        if wrap_mode is not None:
            self.set_wrap_mode(0, wrap_mode)
            self.set_wrap_mode(1, wrap_mode)
            self.set_wrap_mode(2, wrap_mode)

        if read_mode is not None:
            self.set_read_mode(read_mode)

        if filter_mode is not None:
            if OPTIX_VERSION >= 3090 and buffer.get_mip_level_count() > 1:
                self.set_filtering_modes(filter_mode, filter_mode, filter_mode)
            else:
                self.set_filtering_modes(filter_mode, filter_mode, RTfiltermode.RT_FILTER_NONE)

        self.set_max_anisotropy(max_anisotropy)

        if OPTIX_VERSION < 3090:
            # required with OptiX < 3.9.0
            self.set_mip_level_count(1)
            self.set_array_size(1)

        self.set_buffer(0, 0, buffer)

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

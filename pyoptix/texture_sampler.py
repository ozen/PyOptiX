from pyoptix._driver import OPTIX_VERSION
from pyoptix.enums import FilterMode, convert_filtering_mode, convert_wrap_mode, convert_read_mode, \
    convert_indexing_mode
from pyoptix.context import current_context
from pyoptix.mixins.bindless import BindlessMixin
from pyoptix.mixins.destroyable import DestroyableObject
from pyoptix.mixins.hascontext import HasContextMixin


class TextureSampler(HasContextMixin, DestroyableObject, BindlessMixin):
    def __init__(self, buffer, wrap_mode=None, indexing_mode=None,
                 read_mode=None, filter_mode=None, max_anisotropy=1):
        HasContextMixin.__init__(self, current_context())
        DestroyableObject.__init__(self, self._safe_context._create_texture_sampler())
        BindlessMixin.__init__(self)

        self._buffer = None
        self._filtering_mode_minification = None
        self._filtering_mode_magnification = None
        self._filtering_mode_mipmapping = None

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
                self.set_filtering_modes(filter_mode, filter_mode, FilterMode.none)

        self._safe_native.set_max_anisotropy(max_anisotropy)

        if OPTIX_VERSION < 3090:
            # required with OptiX < 3.9.0
            self._safe_native.set_mip_level_count(1)
            self._safe_native.set_array_size(1)

        self.set_buffer(0, 0, buffer)

    @property
    def id(self):
        return self.get_id()

    def get_id(self):
        return self._safe_native.get_id()

    def set_buffer(self, texture_array_idx, mip_level, buffer):
        self._buffer = buffer
        self._safe_native.set_buffer(texture_array_idx, mip_level, buffer._safe_native)

    def get_buffer(self):
        return self._buffer

    def set_filtering_modes(self, minification=None, magnification=None, mipmapping=None):
        minification = convert_filtering_mode(minification)
        magnification = convert_filtering_mode(magnification)
        mipmapping = convert_filtering_mode(mipmapping)

        if minification is None:
            minification = FilterMode.none

        if magnification is None:
            magnification = FilterMode.none

        if mipmapping is None:
            mipmapping = FilterMode.none

        self._filtering_mode_minification = minification
        self._filtering_mode_magnification = magnification
        self._filtering_mode_mipmapping = mipmapping

        self._safe_native.set_filtering_modes(minification, magnification, mipmapping)

    def get_filtering_modes(self):
        return self._filtering_mode_minification, self._filtering_mode_magnification, self._filtering_mode_mipmapping

    def set_wrap_mode(self, dim, mode):
        mode = convert_wrap_mode(mode)
        self._safe_native.set_wrap_mode(dim, mode)

    def get_wrap_mode(self):
        return self._safe_native.get_wrap_mode()

    def set_read_mode(self, mode):
        mode = convert_read_mode(mode)
        self._safe_native.set_read_mode(mode)

    def get_read_mode(self):
        return self._safe_native.get_read_mode()

    def set_indexing_mode(self, mode):
        mode = convert_indexing_mode(mode)
        self._safe_native.set_indexing_mode(mode)

    def get_indexing_mode(self):
        return self._safe_native.get_indexing_mode()

    def set_max_anisotropy(self, max_anisotropy):
        self._safe_native.set_max_anisotropy(max_anisotropy)

    def get_max_anisotropy(self):
        return self._safe_native.get_max_anisotropy()

    def set_mip_level_clamp(self, mip_level_clamp):
        self._safe_native.set_mip_level_clamp(mip_level_clamp)

    def get_mip_level_clamp(self):
        return self._safe_native.get_mip_level_clamp()

    def set_mip_level_bias(self, mip_level_bias):
        self._safe_native.set_mip_level_bias(mip_level_bias)

    def get_mip_level_bias(self):
        return self._safe_native.get_mip_level_bias()

    def validate(self):
        self._safe_native.validate()

from pyoptix._driver import OPTIX_VERSION, RTfiltermode
from pyoptix.objects import TextureSamplerObj
from pyoptix.highlevel.shared import context


class TextureSampler(TextureSamplerObj):
    def __init__(self, buffer, wrap_mode=None, indexing_mode=None,
                 read_mode=None, filter_mode=None, max_anisotropy=1):
        native = context._create_texture_sampler()
        TextureSamplerObj.__init__(self, native=native, context=context)

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

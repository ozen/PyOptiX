from pyoptix._driver import _OptixTextureSamplerWrapper, RTfiltermode, RTwrapmode, RTtexturereadmode, RTtextureindexmode
from pyoptix.objects.commons.optix_object import OptixObject


WRAP_STRING_TO_OPTIX_ENUM = {
    'repeat': RTwrapmode.RT_WRAP_REPEAT,
    'clamp': RTwrapmode.RT_WRAP_CLAMP_TO_EDGE,
    'mirror': RTwrapmode.RT_WRAP_MIRROR,
    'clamp_to_border': RTwrapmode.RT_WRAP_CLAMP_TO_BORDER,
}

FILTERING_STRING_TO_OPTIX_ENUM = {
    'nearest': RTfiltermode.RT_FILTER_NEAREST,
    'linear': RTfiltermode.RT_FILTER_LINEAR,
    'none': RTfiltermode.RT_FILTER_NONE,
}

READ_STRING_TO_OPTIX_ENUM = {
    'element': RTtexturereadmode.RT_TEXTURE_READ_ELEMENT_TYPE,
    'normalized_float': RTtexturereadmode.RT_TEXTURE_READ_NORMALIZED_FLOAT,
}

INDEXING_STRING_TO_OPTIX_ENUM = {
    'normalized': RTtextureindexmode.RT_TEXTURE_INDEX_NORMALIZED_COORDINATES,
    'index': RTtextureindexmode.RT_TEXTURE_INDEX_ARRAY_INDEX,
}


def convert_wrap_mode(string):
    if isinstance(string, str) and string.lower() in WRAP_STRING_TO_OPTIX_ENUM:
        return WRAP_STRING_TO_OPTIX_ENUM[string]
    else:
        return string


def convert_filtering_mode(string):
    if isinstance(string, str) and string.lower() in FILTERING_STRING_TO_OPTIX_ENUM:
        return FILTERING_STRING_TO_OPTIX_ENUM[string]
    else:
        return string


def convert_read_mode(string):
    if isinstance(string, str) and string.lower() in READ_STRING_TO_OPTIX_ENUM:
        return READ_STRING_TO_OPTIX_ENUM[string]
    else:
        return string


def convert_indexing_mode(string):
    if isinstance(string, str) and string.lower() in INDEXING_STRING_TO_OPTIX_ENUM:
        return INDEXING_STRING_TO_OPTIX_ENUM[string]
    else:
        return string


class OptixTextureSampler(_OptixTextureSamplerWrapper, OptixObject):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixTextureSamplerWrapper.__init__(self, native)
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

        if not minification:
            minification = RTfiltermode.RT_FILTER_NONE

        if not magnification:
            magnification = RTfiltermode.RT_FILTER_NONE

        if not mipmapping:
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

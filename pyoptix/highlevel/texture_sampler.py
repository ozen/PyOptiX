from pyoptix.objects import TextureSamplerObj
from pyoptix.highlevel.shared import context


class TextureSampler(TextureSamplerObj):
    def __init__(self, buffer, wrap_mode=None, indexing_mode=None,
                 read_mode=None, filter_mode=None, max_anisotropy=1):
        internal = context.create_texture_sampler(buffer=buffer,
                                                  wrap_mode=wrap_mode,
                                                  indexing_mode=indexing_mode,
                                                  read_mode=read_mode,
                                                  filter_mode=filter_mode,
                                                  max_anisotropy=max_anisotropy)
        TextureSamplerObj.__init__(self, native=internal.native, context=context)

#pragma once
#include "shared_includes.h"
#include "buffer.h"
#include "destroyable.h"


class NativeTextureSamplerWrapper : public NativeDestroyableWrapper
{
private:
    optix::TextureSampler texture_sampler;

public:
    NativeTextureSamplerWrapper(optix::TextureSampler texture_sampler);
    ~NativeTextureSamplerWrapper();
    int get_id();
    void set_mip_level_clamp(float min_level, float max_level);
    std::vector<float> get_mip_level_clamp();
    void set_mip_level_bias(float bias_value);
    float get_mip_level_bias();
    void set_mip_level_count(unsigned int num_mip_levels);
    unsigned int get_mip_level_count();
    void set_array_size(unsigned int  num_textures_in_array);
    unsigned int get_array_size();
    void set_wrap_mode(unsigned int dim, RTwrapmode wrapmode);
    RTwrapmode get_wrap_mode(unsigned int dim);
    void set_max_anisotropy(float value);
    float get_max_anisotropy();
    void set_read_mode(RTtexturereadmode readmode);
    RTtexturereadmode get_read_mode();
    void set_indexing_mode(RTtextureindexmode indexmode);
    RTtextureindexmode get_indexing_mode();
    void set_filtering_modes(RTfiltermode minification, RTfiltermode magnification, RTfiltermode mipmapping);
    void set_buffer(unsigned int texture_array_idx, unsigned int mip_level, NativeBufferWrapper* buffer);
    optix::TextureSampler get_native();
    static void boost_python_expose();
};

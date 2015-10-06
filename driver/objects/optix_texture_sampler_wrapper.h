#ifndef OPTIX_TEXTURE_SAMPLER_WRAPPER_H
#define OPTIX_TEXTURE_SAMPLER_WRAPPER_H

#include "shared_includes.h"
#include "optix_buffer_wrapper.h"


#include "optix_destroyable_object_wrapper.h"


class OptixTextureSamplerWrapper: public OptixDestroyableObject
{
private:
    optix::TextureSampler texture_sampler;

public:
    OptixTextureSamplerWrapper(optix::TextureSampler texture_sampler);
    ~OptixTextureSamplerWrapper();

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

    int get_id();
    void set_buffer(unsigned int texture_array_idx, unsigned int mip_level, OptixBufferWrapper* buffer);

    optix::TextureSampler get_native();

    static void export_for_python();
};


#endif

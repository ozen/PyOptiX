#include "optix_texture_sampler_wrapper.h"
#include "Python.h"
#include <boost/python.hpp>


OptixTextureSamplerWrapper::OptixTextureSamplerWrapper(optix::TextureSampler texture_sampler)
{
    this->texture_sampler = texture_sampler;
    this->set_destroyable_object(this->texture_sampler.get());
}

OptixTextureSamplerWrapper::~OptixTextureSamplerWrapper()
{
    if(this->texture_sampler.get() != 0)
        this->texture_sampler->destroy();
}

void OptixTextureSamplerWrapper::set_mip_level_clamp(float min_level, float max_level)
{
    #if OPTIX_VERSION < 3090
        PyErr_SetString(PyExc_NotImplementedError, "OptiX versions before 3.9.0 don't have mipmapping functions");
        boost::python::throw_error_already_set();
    #else
        this->texture_sampler->setMipLevelClamp(min_level, max_level);
    #endif
}

std::vector<float> OptixTextureSamplerWrapper::get_mip_level_clamp()
{
    #if OPTIX_VERSION < 3090
        PyErr_SetString(PyExc_NotImplementedError, "OptiX versions before 3.9.0 don't have mipmapping functions");
        boost::python::throw_error_already_set();
        return std::vector<float>();
    #else
        std::vector<float> res = std::vector<float>();
        float min_level, max_level;
        this->texture_sampler->getMipLevelClamp(min_level, max_level);
        res.push_back(float(min_level));
        res.push_back(float(max_level));
        return res;
    #endif
}

void OptixTextureSamplerWrapper::set_mip_level_bias(float bias_value)
{
    #if OPTIX_VERSION < 3090
        PyErr_SetString(PyExc_NotImplementedError, "OptiX versions before 3.9.0 don't have mipmapping functions");
        boost::python::throw_error_already_set();
    #else
        this->texture_sampler->setMipLevelBias(bias_value);
    #endif
}

float OptixTextureSamplerWrapper::get_mip_level_bias()
{
    #if OPTIX_VERSION < 3090
        PyErr_SetString(PyExc_NotImplementedError, "OptiX versions before 3.9.0 don't have mipmapping functions");
        boost::python::throw_error_already_set();
        return 0.0;
    #else
        return this->texture_sampler->getMipLevelBias();
    #endif
}

void OptixTextureSamplerWrapper::set_mip_level_count(unsigned int num_mip_levels)
{
    this->texture_sampler->setMipLevelCount(num_mip_levels);
}

unsigned int OptixTextureSamplerWrapper::get_mip_level_count()
{
    return this->texture_sampler->getMipLevelCount();
}

void OptixTextureSamplerWrapper::set_array_size(unsigned int num_textures_in_array)
{
    this->texture_sampler->setArraySize(num_textures_in_array);
}

unsigned int OptixTextureSamplerWrapper::get_array_size()
{
    return this->texture_sampler->getArraySize();
}

void OptixTextureSamplerWrapper::set_wrap_mode(unsigned int dim, RTwrapmode wrapmode)
{
    this->texture_sampler->setWrapMode(dim, wrapmode);
}

RTwrapmode OptixTextureSamplerWrapper::get_wrap_mode(unsigned int dim)
{
    return this->texture_sampler->getWrapMode(dim);
}

void OptixTextureSamplerWrapper::set_max_anisotropy(float value)
{
    this->texture_sampler->setMaxAnisotropy(value);
}

float OptixTextureSamplerWrapper::get_max_anisotropy()
{
    return this->texture_sampler->getMaxAnisotropy();
}

void OptixTextureSamplerWrapper::set_read_mode(RTtexturereadmode readmode)
{
    this->texture_sampler->setReadMode(readmode);
}

RTtexturereadmode OptixTextureSamplerWrapper::get_read_mode()
{
    return this->texture_sampler->getReadMode();
}

void OptixTextureSamplerWrapper::set_indexing_mode(RTtextureindexmode indexmode)
{
    this->texture_sampler->setIndexingMode(indexmode);
}

RTtextureindexmode OptixTextureSamplerWrapper::get_indexing_mode()
{
    return this->texture_sampler->getIndexingMode();
}

void OptixTextureSamplerWrapper::set_filtering_modes(RTfiltermode minification, RTfiltermode magnification, RTfiltermode mipmapping)
{
    this->texture_sampler->setFilteringModes(minification, magnification, mipmapping);
}

int OptixTextureSamplerWrapper::get_id()
{
    return this->texture_sampler->getId();
}

void OptixTextureSamplerWrapper::set_buffer(unsigned int texture_array_idx, unsigned int mip_level, OptixBufferWrapper* buffer)
{
    this->texture_sampler->setBuffer(texture_array_idx, mip_level, buffer->get_native_buffer());
}

optix::TextureSampler OptixTextureSamplerWrapper::get_native()
{
    return this->texture_sampler;
}

void OptixTextureSamplerWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixTextureSamplerWrapper, bp::bases<OptixDestroyableObject> >(
                "_OptixTextureSamplerWrapper",
                "_OptixTextureSamplerWrapper docstring",
                bp::init<optix::TextureSampler>())

            .def("get_id", &OptixTextureSamplerWrapper::get_id)

            .def("set_mip_level_clamp", &OptixTextureSamplerWrapper::set_mip_level_clamp)
            .def("get_mip_level_clamp", &OptixTextureSamplerWrapper::get_mip_level_clamp)

            .def("set_mip_level_bias", &OptixTextureSamplerWrapper::set_mip_level_bias)
            .def("get_mip_level_bias", &OptixTextureSamplerWrapper::get_mip_level_bias)

            .def("set_max_anisotropy", &OptixTextureSamplerWrapper::set_max_anisotropy)
            .def("get_max_anisotropy", &OptixTextureSamplerWrapper::get_max_anisotropy)

            .def("set_mip_level_count", &OptixTextureSamplerWrapper::set_mip_level_count)
            .def("get_mip_level_count", &OptixTextureSamplerWrapper::get_mip_level_count)

            .def("set_array_size", &OptixTextureSamplerWrapper::set_array_size)
            .def("get_array_size", &OptixTextureSamplerWrapper::get_array_size)

            .def("_set_wrap_mode", &OptixTextureSamplerWrapper::set_wrap_mode)
            .def("get_wrap_mode", &OptixTextureSamplerWrapper::get_wrap_mode)

            .def("_set_read_mode", &OptixTextureSamplerWrapper::set_read_mode)
            .def("get_read_mode", &OptixTextureSamplerWrapper::get_read_mode)

            .def("_set_indexing_mode", &OptixTextureSamplerWrapper::set_indexing_mode)
            .def("get_indexing_mode", &OptixTextureSamplerWrapper::get_indexing_mode)

            .def("_set_filtering_modes", &OptixTextureSamplerWrapper::set_filtering_modes)

            .def("_set_buffer", &OptixTextureSamplerWrapper::set_buffer);
}


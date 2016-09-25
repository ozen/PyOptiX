#include "texture_sampler.h"


NativeTextureSamplerWrapper::NativeTextureSamplerWrapper(optix::TextureSampler texture_sampler) {
    this->texture_sampler = texture_sampler;
    this->set_destroyable_object(this->texture_sampler.get());
}

void NativeTextureSamplerWrapper::set_mip_level_clamp(float min_level, float max_level) {
    #if OPTIX_VERSION < 3090
        PyErr_SetString(PyExc_NotImplementedError, "OptiX versions before 3.9.0 don't have mipmapping functions");
        boost::python::throw_error_already_set();
    #else
        this->texture_sampler->setMipLevelClamp(min_level, max_level);
    #endif
}

std::vector<float> NativeTextureSamplerWrapper::get_mip_level_clamp() {
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

void NativeTextureSamplerWrapper::set_mip_level_bias(float bias_value) {
    #if OPTIX_VERSION < 3090
        PyErr_SetString(PyExc_NotImplementedError, "OptiX versions before 3.9.0 don't have mipmapping functions");
        boost::python::throw_error_already_set();
    #else
        this->texture_sampler->setMipLevelBias(bias_value);
    #endif
}

float NativeTextureSamplerWrapper::get_mip_level_bias() {
    #if OPTIX_VERSION < 3090
        PyErr_SetString(PyExc_NotImplementedError, "OptiX versions before 3.9.0 don't have mipmapping functions");
        boost::python::throw_error_already_set();
        return 0.0;
    #else
        return this->texture_sampler->getMipLevelBias();
    #endif
}

void NativeTextureSamplerWrapper::set_mip_level_count(unsigned int num_mip_levels) {
    this->texture_sampler->setMipLevelCount(num_mip_levels);
}

unsigned int NativeTextureSamplerWrapper::get_mip_level_count() {
    return this->texture_sampler->getMipLevelCount();
}

void NativeTextureSamplerWrapper::set_array_size(unsigned int num_textures_in_array) {
    this->texture_sampler->setArraySize(num_textures_in_array);
}

unsigned int NativeTextureSamplerWrapper::get_array_size() {
    return this->texture_sampler->getArraySize();
}

void NativeTextureSamplerWrapper::set_wrap_mode(unsigned int dim, RTwrapmode wrapmode) {
    this->texture_sampler->setWrapMode(dim, wrapmode);
}

RTwrapmode NativeTextureSamplerWrapper::get_wrap_mode(unsigned int dim) {
    return this->texture_sampler->getWrapMode(dim);
}

void NativeTextureSamplerWrapper::set_max_anisotropy(float value) {
    this->texture_sampler->setMaxAnisotropy(value);
}

float NativeTextureSamplerWrapper::get_max_anisotropy() {
    return this->texture_sampler->getMaxAnisotropy();
}

void NativeTextureSamplerWrapper::set_read_mode(RTtexturereadmode readmode) {
    this->texture_sampler->setReadMode(readmode);
}

RTtexturereadmode NativeTextureSamplerWrapper::get_read_mode() {
    return this->texture_sampler->getReadMode();
}

void NativeTextureSamplerWrapper::set_indexing_mode(RTtextureindexmode indexmode) {
    this->texture_sampler->setIndexingMode(indexmode);
}

RTtextureindexmode NativeTextureSamplerWrapper::get_indexing_mode() {
    return this->texture_sampler->getIndexingMode();
}

void NativeTextureSamplerWrapper::set_filtering_modes(RTfiltermode minification, RTfiltermode magnification, RTfiltermode mipmapping) {
    this->texture_sampler->setFilteringModes(minification, magnification, mipmapping);
}

int NativeTextureSamplerWrapper::get_id() {
    return this->texture_sampler->getId();
}

void NativeTextureSamplerWrapper::set_buffer(unsigned int texture_array_idx, unsigned int mip_level, NativeBufferWrapper* buffer) {
    this->texture_sampler->setBuffer(texture_array_idx, mip_level, buffer->get_native_buffer());
}

optix::TextureSampler NativeTextureSamplerWrapper::get_native() {
    return this->texture_sampler;
}

void NativeTextureSamplerWrapper::export_for_python() {
    boost::python::class_<NativeTextureSamplerWrapper, boost::python::bases<NativeDestroyableWrapper> >(
                "NativeTextureSamplerWrapper",
                "NativeTextureSamplerWrapper docstring",
                boost::python::init<optix::TextureSampler>())

            .def("get_id", &NativeTextureSamplerWrapper::get_id)
            .def("set_mip_level_clamp", &NativeTextureSamplerWrapper::set_mip_level_clamp)
            .def("get_mip_level_clamp", &NativeTextureSamplerWrapper::get_mip_level_clamp)
            .def("set_mip_level_bias", &NativeTextureSamplerWrapper::set_mip_level_bias)
            .def("get_mip_level_bias", &NativeTextureSamplerWrapper::get_mip_level_bias)
            .def("set_max_anisotropy", &NativeTextureSamplerWrapper::set_max_anisotropy)
            .def("get_max_anisotropy", &NativeTextureSamplerWrapper::get_max_anisotropy)
            .def("set_mip_level_count", &NativeTextureSamplerWrapper::set_mip_level_count)
            .def("get_mip_level_count", &NativeTextureSamplerWrapper::get_mip_level_count)
            .def("set_array_size", &NativeTextureSamplerWrapper::set_array_size)
            .def("get_array_size", &NativeTextureSamplerWrapper::get_array_size)
            .def("_set_wrap_mode", &NativeTextureSamplerWrapper::set_wrap_mode)
            .def("get_wrap_mode", &NativeTextureSamplerWrapper::get_wrap_mode)
            .def("_set_read_mode", &NativeTextureSamplerWrapper::set_read_mode)
            .def("get_read_mode", &NativeTextureSamplerWrapper::get_read_mode)
            .def("_set_indexing_mode", &NativeTextureSamplerWrapper::set_indexing_mode)
            .def("get_indexing_mode", &NativeTextureSamplerWrapper::get_indexing_mode)
            .def("_set_filtering_modes", &NativeTextureSamplerWrapper::set_filtering_modes)
            .def("_set_buffer", &NativeTextureSamplerWrapper::set_buffer);
}

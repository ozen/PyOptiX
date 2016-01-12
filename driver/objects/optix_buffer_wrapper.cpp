#include <iostream>
#include "optix_buffer_wrapper.h"
#include "numpy_boost_helpers.h"


OptixBufferWrapper::OptixBufferWrapper(optix::Buffer buffer)
{
    this->buffer = buffer;
    this->set_destroyable_object(this->buffer.get());
}

OptixBufferWrapper::~OptixBufferWrapper()
{
    if(buffer.get() != 0)
        this->buffer->destroy();
}

int OptixBufferWrapper::get_id()
{
    return this->buffer->getId();
}

void OptixBufferWrapper::mark_dirty()
{
    this->buffer->markDirty();
}

void OptixBufferWrapper::set_format(RTformat format)
{
    this->buffer->setFormat(format);
}

RTformat OptixBufferWrapper::get_format()
{
    return this->buffer->getFormat();
}

void OptixBufferWrapper::set_size(boost::python::list& sizes)
{
    int dim = boost::python::len(sizes);

    std::vector<int> sizes_vector = std::vector<int>();

    for(int i = 0; i < dim; i++)
        sizes_vector.push_back(boost::python::extract<int>(sizes[i]));

    set_size_with_vector_int(sizes_vector);
}

void OptixBufferWrapper::set_size_with_vector_int(std::vector<int> sizes_vector)
{
    int dim = sizes_vector.size();

    if(dim == 1)
        this->buffer->setSize(sizes_vector.at(0));
    else if(dim == 2)
        this->buffer->setSize(sizes_vector.at(0), sizes_vector.at(1));
    else if(dim == 3)
        this->buffer->setSize(sizes_vector.at(0), sizes_vector.at(1), sizes_vector.at(2));
    else
        throw "Not supported buffer size";
}

unsigned long OptixBufferWrapper::get_buffer_size_in_bytes()
{
    std::vector<int> size = this->get_size();
    int element_size = this->buffer->getElementSize();

    if(size.size() == 0)
        return 0;

    unsigned long total_bytes = element_size;

    for(int i = 0; i < size.size(); i++)
        total_bytes *= size.at(i);

    return total_bytes;
}

unsigned long OptixBufferWrapper::get_mip_level_size_in_bytes(unsigned int level)
{
    std::vector<int> size = this->get_mip_level_size(level);
    int element_size = this->buffer->getElementSize();

    if(size.size() == 0)
        return 0;

    unsigned long total_bytes = element_size;

    for(int i = 0; i < size.size(); i++)
        total_bytes *= size.at(i);

    return total_bytes;
}

std::vector<int> OptixBufferWrapper::get_size()
{
    int dim = this->buffer->getDimensionality();
    std::vector<int> res = std::vector<int>();
    RTsize x, y, z;
    this->buffer->getSize(x, y, z);

    if(dim > 0) {
        res.push_back(int(x));
    }
    if(dim > 1) {
        res.push_back(int(y));
    }
    if(dim > 2) {
        res.push_back(int(z));
    }
    return res;
}

void OptixBufferWrapper::set_element_size(int size_in_bytes)
{
    this->buffer->setElementSize(size_in_bytes);
}

int OptixBufferWrapper::get_element_size()
{
    return this->buffer->getElementSize();
}

void OptixBufferWrapper::copy_into_numpy_array(const boost::numpy::ndarray& numpy_array)
{
    void* buff_ptr = this->buffer->map();
    long size_in_bytes = get_array_size_in_bytes(numpy_array);
    memcpy(numpy_array.get_data(), buff_ptr, size_in_bytes);
    this->buffer->unmap();
}

void OptixBufferWrapper::copy_from_numpy_array(const boost::numpy::ndarray& numpy_array)
{
    void* buff_ptr = this->buffer->map();
    long size_in_bytes = get_array_size_in_bytes(numpy_array);
    memcpy(buff_ptr, numpy_array.get_data(), size_in_bytes);
    this->buffer->unmap();
}

void OptixBufferWrapper::copy_mip_level_from_numpy_array(unsigned int level, const boost::numpy::ndarray& numpy_array)
{
    void* buff_ptr = this->buffer->map(level);
    long size_in_bytes = get_array_size_in_bytes(numpy_array);
    memcpy(buff_ptr, numpy_array.get_data(), size_in_bytes);
    this->buffer->unmap(level);
}

unsigned int OptixBufferWrapper::get_mip_level_count()
{
    return this->buffer->getMipLevelCount();
}

void OptixBufferWrapper::set_mip_level_count(unsigned int level_count)
{
    this->buffer->setMipLevelCount(level_count);
}

std::vector<int> OptixBufferWrapper::get_mip_level_size(unsigned int level)
{
    int dim = this->buffer->getDimensionality();
    std::vector<int> res = std::vector<int>();
    RTsize x, y, z;
    this->buffer->getMipLevelSize(level, x, y, z);

    if(dim > 0) {
        res.push_back(int(x));
    }
    if(dim > 1) {
        res.push_back(int(y));
    }
    if(dim > 2) {
        res.push_back(int(z));
    }
    return res;
}

optix::Buffer OptixBufferWrapper::get_native_buffer()
{
    return this->buffer;
}


// *********************************
// *********************************
// PYTHON SUPPORT
// *********************************
// *********************************



void OptixBufferWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixBufferWrapper, bp::bases<OptixDestroyableObject> >(
                "_OptixBufferWrapper",
                "Wrapper for OptixBuffer",
                bp::init<optix::Buffer>())

            .def("get_id", &OptixBufferWrapper::get_id)
            .def("mark_dirty", &OptixBufferWrapper::mark_dirty)

            .def("_set_format", &OptixBufferWrapper::set_format)
            .def("get_format", &OptixBufferWrapper::get_format)

            .def("_set_size", &OptixBufferWrapper::set_size)
            .def("_get_size", &OptixBufferWrapper::get_size)
            .def("_get_size_in_bytes", &OptixBufferWrapper::get_buffer_size_in_bytes)

            .def("_set_element_size", &OptixBufferWrapper::set_element_size)
            .def("_get_element_size", &OptixBufferWrapper::get_element_size)

            .def("_copy_into_numpy_array", &OptixBufferWrapper::copy_into_numpy_array)
            .def("_copy_from_numpy_array", &OptixBufferWrapper::copy_from_numpy_array)
            .def("_copy_mip_level_from_numpy_array", &OptixBufferWrapper::copy_mip_level_from_numpy_array)

            .def("set_mip_level_count", &OptixBufferWrapper::set_mip_level_count)
            .def("get_mip_level_count", &OptixBufferWrapper::get_mip_level_count)

            .def("get_mip_level_size", &OptixBufferWrapper::get_mip_level_size)
            .def("_get_mip_level_size_in_bytes", &OptixBufferWrapper::get_mip_level_size_in_bytes);
}

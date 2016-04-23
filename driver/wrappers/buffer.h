#pragma once
#include "shared_includes.h"
#include "destroyable.h"


class NativeBufferWrapper : public NativeDestroyableWrapper
{
private:
    optix::Buffer buffer;

public:
    NativeBufferWrapper(optix::Buffer buffer);
    ~NativeBufferWrapper();
    int get_id();
    void mark_dirty();
    void set_format(RTformat format);
    RTformat get_format();
    std::vector<int> get_size();
    void set_size(boost::python::list& sizes);
    void set_size_with_vector_int(std::vector<int> sizes_vector);
    unsigned long get_buffer_size_in_bytes();
    unsigned long get_mip_level_size_in_bytes(unsigned int level);
    void set_element_size(int size_in_bytes);
    int get_element_size();
    void copy_into_numpy_array(const boost::numpy::ndarray& numpy_array);
    void copy_from_numpy_array(const boost::numpy::ndarray& numpy_array);
    void copy_mip_level_from_numpy_array(unsigned int level, const boost::numpy::ndarray& numpy_array);
    unsigned int get_mip_level_count();
    void set_mip_level_count(unsigned int level_count);
    std::vector<int> get_mip_level_size(unsigned int level);
    optix::Buffer get_native_buffer();
    static void export_for_python();
};

#ifndef OPTIX_BUFFER_WRAPPER_H
#define OPTIX_BUFFER_WRAPPER_H


#include "shared_includes.h"

#include "Python.h"
#include <boost/python.hpp>
#include <boost/numpy.hpp>

#include "optix_destroyable_object_wrapper.h"

class OptixBufferWrapper: public OptixDestroyableObject
{
private:
    optix::Buffer buffer;

public:
    OptixBufferWrapper(optix::Buffer buffer);
    ~OptixBufferWrapper();

    int get_id();
    void mark_dirty();

    // Main
    void set_format(RTformat format);
    RTformat get_format();
    void set_shape(boost::python::list& sizes);
    void set_shape_with_vector_int(std::vector<int> sizes_vector);

    unsigned long get_buffer_size_in_bytes();

    std::vector<int> get_shape();


    void set_element_size(int size_in_bytes);
    int get_element_size();

    //Numpy Support
    void copy_into_numpy_array(const boost::numpy::ndarray& numpy_array);
    void copy_from_numpy_array(const boost::numpy::ndarray& numpy_array);

    optix::Buffer get_native_buffer();

    static void export_for_python();
};



#endif

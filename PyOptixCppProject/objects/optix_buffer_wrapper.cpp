#include "optix_buffer_wrapper.h"
#include <iostream>


OptixBufferWrapper::OptixBufferWrapper(optix::Buffer buffer)
{
    this->buffer = buffer;
    this->set_destroyable_object(this->buffer.get());
}

OptixBufferWrapper::~OptixBufferWrapper()
{
    std::cout<<"OptixBufferWrapper deconstruction"<<std::endl;
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

void OptixBufferWrapper::set_shape(boost::python::list& sizes)
{
    int dim = boost::python::len(sizes);

    std::vector<int> sizes_vector = std::vector<int>();

    for(int i = 0; i < dim; i++)
        sizes_vector.push_back(boost::python::extract<int>(sizes[i]));

    set_shape_with_vector_int(sizes_vector);
}

void OptixBufferWrapper::set_shape_with_vector_int(std::vector<int> sizes_vector)
{
    int dim = sizes_vector.size();

    if( dim == 1)
        this->buffer->setSize(sizes_vector.at(0));
    else if( dim == 2)
        this->buffer->setSize(sizes_vector.at(0), sizes_vector.at(1));
    else if(dim == 3)
        this->buffer->setSize(sizes_vector.at(0), sizes_vector.at(1), sizes_vector.at(2));
    else
        throw "Not supported buffer size";
}

unsigned long OptixBufferWrapper::get_buffer_size_in_bytes()
{
    std::vector<int> shape = this->get_shape();
    int element_size = this->buffer->getElementSize();

    if(shape.size() == 0)
        return 0;

    unsigned long total_bytes = element_size;

    for(int i = 0; i < shape.size(); i++)
        total_bytes *= shape.at(i);

    return total_bytes;
}

std::vector<int> OptixBufferWrapper::get_shape()
{
    int dim = this->buffer->getDimensionality();
    std::vector<int> list = std::vector<int>();
    RTsize x;
    RTsize y;
    RTsize z;
    this->buffer->getSize(x, y, z);

    if( dim > 0)
    {
        list.push_back(int(x));
    }
    if(dim > 1)
    {
        list.push_back(int(y));
    }
    if(dim > 2)
    {
        list.push_back(int(z));
    }
    return list;
}

void OptixBufferWrapper::set_element_size(int size_in_bytes)
{
    this->buffer->setElementSize(size_in_bytes);
}

int OptixBufferWrapper::get_element_size()
{
    return this->buffer->getElementSize();
}


#include "numpy_boost_helpers.h"
//Numpy Support
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
                "_OptixBufferWrapper docstring",
                bp::init<optix::Buffer>())

            //*****************
            // DIRECT ACCESS
            //*****************
            .def("get_id", &OptixBufferWrapper::get_id)
            .def("mark_dirty", &OptixBufferWrapper::mark_dirty)

            .add_property("nbytes", &OptixBufferWrapper::get_buffer_size_in_bytes)

            //*****************
            // CONTROLLED ACCESS
            //*****************
            .def("_get_format", &OptixBufferWrapper::get_format)
            .def("_set_format", &OptixBufferWrapper::set_format)

            .def("_get_shape", &OptixBufferWrapper::get_shape)
            .def("_set_shape", &OptixBufferWrapper::set_shape)

            .def("_set_element_size", &OptixBufferWrapper::set_element_size)
            .def("_get_element_size", &OptixBufferWrapper::get_element_size)

            .def("_copy_into_numpy_array", &OptixBufferWrapper::copy_into_numpy_array)
            .def("_copy_from_numpy_array", &OptixBufferWrapper::copy_from_numpy_array);
}

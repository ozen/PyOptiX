#include "buffer.h"


NativeBufferWrapper::NativeBufferWrapper(optix::Buffer buffer) {
    this->buffer = buffer;
    this->set_destroyable_object(this->buffer.get());
}

NativeBufferWrapper::~NativeBufferWrapper() {
    if (!is_destroyed && auto_destroy) this->buffer->destroy();
}

int NativeBufferWrapper::get_id() {
    return this->buffer->getId();
}

void NativeBufferWrapper::mark_dirty() {
    this->buffer->markDirty();
}

void NativeBufferWrapper::set_format(RTformat format) {
    this->buffer->setFormat(format);
}

RTformat NativeBufferWrapper::get_format() {
    return this->buffer->getFormat();
}

void NativeBufferWrapper::set_size(boost::python::list& sizes) {
    int dim = boost::python::len(sizes);

    std::vector<int> sizes_vector = std::vector<int>();

    for(int i = 0; i < dim; i++)
        sizes_vector.push_back(boost::python::extract<int>(sizes[i]));

    set_size_with_vector_int(sizes_vector);
}

void NativeBufferWrapper::set_size_with_vector_int(std::vector<int> sizes_vector) {
    int dim = sizes_vector.size();

    if(dim == 1)
        this->buffer->setSize(sizes_vector.at(0));
    else if(dim == 2)
        this->buffer->setSize(sizes_vector.at(0), sizes_vector.at(1));
    else if(dim == 3)
        this->buffer->setSize(sizes_vector.at(0), sizes_vector.at(1), sizes_vector.at(2));
    else {
        PyErr_SetString(PyExc_ValueError, "Invalid number of dimensions");
        boost::python::throw_error_already_set();
    }
}

unsigned long NativeBufferWrapper::get_buffer_size_in_bytes() {
    std::vector<int> size = this->get_size();
    int element_size = this->buffer->getElementSize();

    if(size.size() == 0)
        return 0;

    unsigned long total_bytes = element_size;

    for(unsigned int i = 0; i < size.size(); i++)
        total_bytes *= size.at(i);

    return total_bytes;
}

unsigned long NativeBufferWrapper::get_mip_level_size_in_bytes(unsigned int level) {
    std::vector<int> size = this->get_mip_level_size(level);
    int element_size = this->buffer->getElementSize();

    if(size.size() == 0)
        return 0;

    unsigned long total_bytes = element_size;

    for(unsigned int i = 0; i < size.size(); i++)
        total_bytes *= size.at(i);

    return total_bytes;
}

std::vector<int> NativeBufferWrapper::get_size() {
    int dim = this->buffer->getDimensionality();
    std::vector<int> res = std::vector<int>();
    RTsize x, y, z;
    this->buffer->getSize(x, y, z);

    if (dim > 0) {
        res.push_back(int(x));
    }
    if (dim > 1) {
        res.push_back(int(y));
    }
    if (dim > 2) {
        res.push_back(int(z));
    }
    return res;
}

void NativeBufferWrapper::set_element_size(int size_in_bytes) {
    this->buffer->setElementSize(size_in_bytes);
}

int NativeBufferWrapper::get_element_size() {
    return this->buffer->getElementSize();
}

void NativeBufferWrapper::copy_into_array(PyObject* array) {
    void* buff_ptr = this->buffer->map();
    Py_buffer pb;
    PyObject_GetBuffer(array, &pb, PyBUF_SIMPLE);
    memcpy(pb.buf, buff_ptr, pb.len);
    PyBuffer_Release(&pb);
    this->buffer->unmap();
}

void NativeBufferWrapper::copy_from_array(PyObject* array) {
    void* buff_ptr = this->buffer->map();
    Py_buffer pb;
    PyObject_GetBuffer(array, &pb, PyBUF_SIMPLE);
    memcpy(buff_ptr, pb.buf, pb.len);
    PyBuffer_Release(&pb);
    this->buffer->unmap();
}

void NativeBufferWrapper::copy_mip_level_from_array(unsigned int level, PyObject* array) {
    #if OPTIX_VERSION < 3090
        PyErr_SetString(PyExc_NotImplementedError, "OptiX versions before 3.9.0 don't have mipmapping functions");
        boost::python::throw_error_already_set();
    #else
        void* buff_ptr = this->buffer->map(level);
        Py_buffer pb;
        PyObject_GetBuffer(array, &pb, PyBUF_SIMPLE);
        memcpy(buff_ptr, pb.buf, pb.len);
        PyBuffer_Release(&pb);
        this->buffer->unmap(level);
    #endif
}

unsigned int NativeBufferWrapper::get_mip_level_count() {
    #if OPTIX_VERSION < 3090
        PyErr_SetString(PyExc_NotImplementedError, "OptiX versions before 3.9.0 don't have mipmapping functions");
        boost::python::throw_error_already_set();
        return 0;
    #else
        return this->buffer->getMipLevelCount();
    #endif
}

void NativeBufferWrapper::set_mip_level_count(unsigned int level_count) {
    #if OPTIX_VERSION < 3090
        PyErr_SetString(PyExc_NotImplementedError, "OptiX versions before 3.9.0 don't have mipmapping functions");
        boost::python::throw_error_already_set();
    #else
        this->buffer->setMipLevelCount(level_count);
    #endif
}

std::vector<int> NativeBufferWrapper::get_mip_level_size(unsigned int level) {
    #if OPTIX_VERSION < 3090
        PyErr_SetString(PyExc_NotImplementedError, "OptiX versions before 3.9.0 don't have mipmapping functions");
        boost::python::throw_error_already_set();
        return std::vector<int>();
    #else
        int dim = this->buffer->getDimensionality();
        std::vector<int> res = std::vector<int>();
        RTsize x, y, z;
        this->buffer->getMipLevelSize(level, x, y, z);

        if (dim > 0) {
            res.push_back(int(x));
        }
        if (dim > 1) {
            res.push_back(int(y));
        }
        if (dim > 2) {
            res.push_back(int(z));
        }
        return res;
    #endif
}

optix::Buffer NativeBufferWrapper::get_native_buffer() {
    return this->buffer;
}

void NativeBufferWrapper::boost_python_expose() {
    boost::python::class_<NativeBufferWrapper, boost::python::bases<NativeDestroyableWrapper> >(
                "NativeBufferWrapper",
                "Wraps optix::Buffer class",
                boost::python::no_init)

            .def("get_id", &NativeBufferWrapper::get_id)
            .def("mark_dirty", &NativeBufferWrapper::mark_dirty)
            .def("set_format", &NativeBufferWrapper::set_format)
            .def("get_format", &NativeBufferWrapper::get_format)
            .def("set_size", &NativeBufferWrapper::set_size)
            .def("get_size", &NativeBufferWrapper::get_size)
            .def("get_size_in_bytes", &NativeBufferWrapper::get_buffer_size_in_bytes)
            .def("set_element_size", &NativeBufferWrapper::set_element_size)
            .def("get_element_size", &NativeBufferWrapper::get_element_size)
            .def("copy_into_array", &NativeBufferWrapper::copy_into_array)
            .def("copy_from_array", &NativeBufferWrapper::copy_from_array)
            .def("copy_mip_level_from_array", &NativeBufferWrapper::copy_mip_level_from_array)
            .def("set_mip_level_count", &NativeBufferWrapper::set_mip_level_count)
            .def("get_mip_level_count", &NativeBufferWrapper::get_mip_level_count)
            .def("get_mip_level_size", &NativeBufferWrapper::get_mip_level_size)
            .def("get_mip_level_size_in_bytes", &NativeBufferWrapper::get_mip_level_size_in_bytes);
}

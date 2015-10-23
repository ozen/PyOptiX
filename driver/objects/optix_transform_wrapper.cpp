#include "optix_transform_wrapper.h"
#include "optix_group_wrapper.h"
#include "optix_selector_wrapper.h"
#include "optix_geometry_group_wrapper.h"
#include "Python.h"
#include <boost/python.hpp>

namespace p = boost::python;
namespace np = boost::numpy;

OptixTransformWrapper::OptixTransformWrapper(optix::Transform transform)
{
    this->transform = transform;
    this->set_destroyable_object(this->transform.get());
}

OptixTransformWrapper::~OptixTransformWrapper()
{
    if(this->transform.get() != 0)
        this->transform->destroy();
}

void OptixTransformWrapper::set_matrix(bool transpose, const np::ndarray& array)
{
    if (array.get_dtype() != np::dtype::get_builtin<float>()) {
        PyErr_SetString(PyExc_TypeError, "Transformation matrix must have float dtype");
        p::throw_error_already_set();
    }

    if (array.get_nd() != 2) {
        PyErr_SetString(PyExc_TypeError, "Transformation matrix must be two dimensional");
        p::throw_error_already_set();
    }

    if (array.shape(0) != 4 || array.shape(1) != 4) {
        PyErr_SetString(PyExc_TypeError, "Transformation matrix must be 4 by 4");
        p::throw_error_already_set();
    }

    this->transform->setMatrix(transpose, reinterpret_cast<float*>(array.get_data()), NULL);

}

np::ndarray OptixTransformWrapper::get_matrix(bool transpose)
{
    np::dtype dt = np::dtype::get_builtin<float>();
    p::tuple shape = p::make_tuple(4,4);
    np::ndarray arr = np::zeros(shape, dt);
    this->transform->getMatrix(transpose, reinterpret_cast<float*>(arr.get_data()), NULL);
    return arr;
}

void OptixTransformWrapper::set_child_geometry_group(unsigned int index, OptixGeometryGroupWrapper* child)
{
    this->transform->setChild(child->get_native());
}

void OptixTransformWrapper::set_child_group(unsigned int index, OptixGroupWrapper* child)
{
    this->transform->setChild(child->get_native());
}

void OptixTransformWrapper::set_child_selector(unsigned int index, OptixSelectorWrapper* child)
{
    this->transform->setChild(child->get_native());
}

void OptixTransformWrapper::set_child_transform(unsigned int index, OptixGeometryGroupWrapper* child)
{
    this->transform->setChild(child->get_native());
}

optix::Transform OptixTransformWrapper::get_native()
{
    return this->transform;
}

void OptixTransformWrapper::export_for_python()
{
    p::class_<OptixTransformWrapper, p::bases<OptixDestroyableObject> >(
                "_OptixTransformWrapper",
                "_OptixTransformWrapper docstring",
                p::init<optix::Transform>())

            .def("set_matrix", &OptixTransformWrapper::set_matrix)
            .def("get_matrix", &OptixTransformWrapper::get_matrix)
            .def("_set_child_geometry_group", &OptixTransformWrapper::set_child_geometry_group)
            .def("_set_child_group", &OptixTransformWrapper::set_child_group)
            .def("_set_child_selector", &OptixTransformWrapper::set_child_selector)
            .def("_set_child_transform", &OptixTransformWrapper::set_child_transform);
}


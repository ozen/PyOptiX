#include "transform.h"
#include "selector.h"
#include "group.h"
#include "geometry_group.h"


NativeTransformWrapper::NativeTransformWrapper(optix::Transform transform) {
    this->transform = transform;
    this->set_destroyable_object(this->transform.get());
}

NativeTransformWrapper::~NativeTransformWrapper() {
    if(this->transform.get() != 0) this->transform->destroy();
}

void NativeTransformWrapper::set_matrix(bool transpose, const boost::numpy::ndarray& array) {
    if (array.get_dtype() != boost::numpy::dtype::get_builtin<float>()) {
        PyErr_SetString(PyExc_ValueError, "Transformation matrix must have float dtype");
        boost::python::throw_error_already_set();
    }

    if (array.get_nd() != 2) {
        PyErr_SetString(PyExc_ValueError, "Transformation matrix must be two dimensional");
        boost::python::throw_error_already_set();
    }

    if (array.shape(0) != 4 || array.shape(1) != 4) {
        PyErr_SetString(PyExc_ValueError, "Transformation matrix must be 4 by 4");
        boost::python::throw_error_already_set();
    }

    this->transform->setMatrix(transpose, reinterpret_cast<float*>(array.get_data()), NULL);

}

boost::numpy::ndarray NativeTransformWrapper::get_matrix(bool transpose) {
    boost::numpy::dtype dt = boost::numpy::dtype::get_builtin<float>();
    boost::python::tuple shape = boost::python::make_tuple(4,4);
    boost::numpy::ndarray arr = boost::numpy::zeros(shape, dt);
    this->transform->getMatrix(transpose, reinterpret_cast<float*>(arr.get_data()), NULL);
    return arr;
}

void NativeTransformWrapper::set_child_geometry_group(unsigned int index, NativeGeometryGroupWrapper* child) {
    this->transform->setChild(child->get_native());
}

void NativeTransformWrapper::set_child_group(unsigned int index, NativeGroupWrapper* child) {
    this->transform->setChild(child->get_native());
}

void NativeTransformWrapper::set_child_selector(unsigned int index, NativeSelectorWrapper* child) {
    this->transform->setChild(child->get_native());
}

void NativeTransformWrapper::set_child_transform(unsigned int index, NativeGeometryGroupWrapper* child) {
    this->transform->setChild(child->get_native());
}

optix::Transform NativeTransformWrapper::get_native() {
    return this->transform;
}

void NativeTransformWrapper::export_for_python() {
    boost::python::class_<NativeTransformWrapper, boost::python::bases<NativeDestroyableWrapper> >(
                "NativeTransformWrapper",
                "NativeTransformWrapper docstring",
                boost::python::init<optix::Transform>())

            .def("set_matrix", &NativeTransformWrapper::set_matrix)
            .def("get_matrix", &NativeTransformWrapper::get_matrix)
            .def("_set_child_geometry_group", &NativeTransformWrapper::set_child_geometry_group)
            .def("_set_child_group", &NativeTransformWrapper::set_child_group)
            .def("_set_child_selector", &NativeTransformWrapper::set_child_selector)
            .def("_set_child_transform", &NativeTransformWrapper::set_child_transform);
}

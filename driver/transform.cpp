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

void NativeTransformWrapper::set_matrix(bool transpose, boost::python::list& matrix) {
    float flat_matrix[16];
    int i, j;

    for (i=0; i<4; i++) {
        for (j=0; j<4; j++) {
            flat_matrix[4*i+j] = boost::python::extract<float>(matrix[i][j]);
        }
    }

    this->transform->setMatrix(transpose, flat_matrix, NULL);
}

boost::python::list NativeTransformWrapper::get_matrix(bool transpose) {
    float flat_matrix[16];
    this->transform->getMatrix(transpose, flat_matrix, NULL);
    boost::python::list matrix;
    int i, j;

    for (i=0; i<4; i++) {
        boost::python::list row;
        for (j=0; j<4; j++) {
            row.append(flat_matrix[4*i+j]);
        }
        matrix.append(row);
    }

    return matrix;
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

            .def("_set_matrix", &NativeTransformWrapper::set_matrix)
            .def("_get_matrix", &NativeTransformWrapper::get_matrix)
            .def("_set_child_geometry_group", &NativeTransformWrapper::set_child_geometry_group)
            .def("_set_child_group", &NativeTransformWrapper::set_child_group)
            .def("_set_child_selector", &NativeTransformWrapper::set_child_selector)
            .def("_set_child_transform", &NativeTransformWrapper::set_child_transform);
}

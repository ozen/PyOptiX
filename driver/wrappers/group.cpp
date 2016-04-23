#include "group.h"
#include "geometry_group.h"
#include "selector.h"


NativeGroupWrapper::NativeGroupWrapper(optix::Group group) {
    this->group = group;
    this->set_destroyable_object(this->group.get());
}

NativeGroupWrapper::~NativeGroupWrapper() {
    if(this->group.get() != 0) this->group->destroy();
}

void NativeGroupWrapper::set_acceleration(NativeAccelerationWrapper* acceleration) {
    this->group->setAcceleration(acceleration->get_native());
}

void NativeGroupWrapper::set_child_count(unsigned int count) {
    this->group->setChildCount(count);
}

unsigned int NativeGroupWrapper::get_child_count() {
    return this->group->getChildCount();
}

void NativeGroupWrapper::set_child_geometry_group(unsigned int index, NativeGeometryGroupWrapper* child) {
    this->group->setChild(index, child->get_native());
}

void NativeGroupWrapper::set_child_group(unsigned int index, NativeGroupWrapper* child) {
    this->group->setChild(index, child->get_native());
}

void NativeGroupWrapper::set_child_selector(unsigned int index, NativeSelectorWrapper* child) {
    this->group->setChild(index, child->get_native());
}

void NativeGroupWrapper::set_child_transform(unsigned int index, NativeTransformWrapper* child) {
    this->group->setChild(index, child->get_native());
}

void NativeGroupWrapper::set_child_acceleration(unsigned int index, NativeAccelerationWrapper* child) {
    this->group->setChild(index, child->get_native());
}

void NativeGroupWrapper::remove_child(unsigned int index) {
    this->group->removeChild(index);
}

optix::Group NativeGroupWrapper::get_native() {
    return this->group;
}

void NativeGroupWrapper::export_for_python()
{
    boost::python::class_<NativeGroupWrapper, boost::python::bases<NativeDestroyableWrapper> >(
                "NativeGroupWrapper",
                "NativeGroupWrapper docstring",
                boost::python::init<optix::Group>())

            .def("_set_acceleration", &NativeGroupWrapper::set_acceleration)
            .def("_set_child_count", &NativeGroupWrapper::set_child_count)
            .def("get_child_count", &NativeGroupWrapper::get_child_count)
            .def("_set_child_geometry_group", &NativeGroupWrapper::set_child_geometry_group)
            .def("_set_child_group", &NativeGroupWrapper::set_child_group)
            .def("_set_child_selector", &NativeGroupWrapper::set_child_selector)
            .def("_set_child_transform", &NativeGroupWrapper::set_child_transform)
            .def("_set_child_acceleration", &NativeGroupWrapper::set_child_acceleration)
            .def("_remove_child", &NativeGroupWrapper::remove_child);
}

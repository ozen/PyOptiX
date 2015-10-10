#include <boost/python.hpp>
#include "optix_group_wrapper.h"


OptixGroupWrapper::OptixGroupWrapper(optix::Group group)
{
    this->group = group;
    this->set_destroyable_object(this->group.get());
}

OptixGroupWrapper::~OptixGroupWrapper()
{
    if(this->group.get() != 0)
        this->group->destroy();
}

void OptixGroupWrapper::set_acceleration(OptixAccelerationWrapper* acceleration)
{
    this->group->setAcceleration(acceleration->get_native());
}

void OptixGroupWrapper::set_child_count(unsigned int count)
{
    this->group->setChildCount(count);
}

unsigned int OptixGroupWrapper::get_child_count()
{
    return this->group->getChildCount();
}

void OptixGroupWrapper::set_child_geometry_group(unsigned int index, OptixGeometryGroupWrapper* child)
{
    this->group->setChild(index, child->get_native());
}

void OptixGroupWrapper::set_child_group(unsigned int index, OptixGroupWrapper* child)
{
    this->group->setChild(index, child->get_native());
}

void OptixGroupWrapper::set_child_selector(unsigned int index, OptixSelectorWrapper* child)
{
    this->group->setChild(index, child->get_native());
}

void OptixGroupWrapper::set_child_transform(unsigned int index, OptixTransformWrapper* child)
{
    this->group->setChild(index, child->get_native());
}

void OptixGroupWrapper::set_child_acceleration(unsigned int index, OptixAccelerationWrapper* child)
{
    this->group->setChild(index, child->get_native());
}

void OptixGroupWrapper::remove_child(unsigned int index)
{
    this->group->removeChild(index);
}

optix::Group OptixGroupWrapper::get_native()
{
    return this->group;
}

void OptixGroupWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixGroupWrapper, bp::bases<OptixDestroyableObject> >(
                "_OptixGroupWrapper",
                "_OptixGroupWrapper docstring",
                bp::init<optix::Group>())

            .def("_set_acceleration", &OptixGroupWrapper::set_acceleration)
            .def("_set_child_count", &OptixGroupWrapper::set_child_count)
            .def("get_child_count", &OptixGroupWrapper::get_child_count)
            .def("_set_child_geometry_group", &OptixGroupWrapper::set_child_geometry_group)
            .def("_set_child_group", &OptixGroupWrapper::set_child_group)
            .def("_set_child_selector", &OptixGroupWrapper::set_child_selector)
            .def("_set_child_transform", &OptixGroupWrapper::set_child_transform)
            .def("_set_child_acceleration", &OptixGroupWrapper::set_child_acceleration)
            .def("_remove_child", &OptixGroupWrapper::remove_child);
}

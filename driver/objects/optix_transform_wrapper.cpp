#include "optix_transform_wrapper.h"

#include "optix_group_wrapper.h"
#include "optix_selector_wrapper.h"
#include "optix_geometry_group_wrapper.h"

OptixTransformWrapper::OptixTransformWrapper(optix::Transform transform)
{
    this->transform = transform;
    this->set_destroyable_object(this->transform.get());
}

OptixTransformWrapper::~OptixTransformWrapper()
{
    std::cout<<"~OptixTransformWrapper deconstruction"<<std::endl;

    if(this->transform.get() != 0)
        this->transform->destroy();
}

void OptixTransformWrapper::set_matrix()
{

}

void OptixTransformWrapper::get_matrix()
{

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

#include "Python.h"
#include <boost/python.hpp>
void OptixTransformWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixTransformWrapper, bp::bases<OptixDestroyableObject> >(
                "_OptixTransformWrapper",
                "_OptixTransformWrapper docstring",
                bp::init<optix::Transform>())
            //*****************
            // DIRECT ACCESS
            //*****************
            .def("_set_matrix", &OptixTransformWrapper::set_matrix)
            .def("_get_matrix", &OptixTransformWrapper::get_matrix)
            .def("_set_child_geometry_group", &OptixTransformWrapper::set_child_geometry_group)
            .def("_set_child_group", &OptixTransformWrapper::set_child_group)
            .def("_set_child_selector", &OptixTransformWrapper::set_child_selector)
            .def("_set_child_transform", &OptixTransformWrapper::set_child_transform);
}


#include "optix_destroyable_object_wrapper.h"
#include "Python.h"
#include <boost/python.hpp>


OptixDestroyableObject::OptixDestroyableObject()
{

}

OptixDestroyableObject::~OptixDestroyableObject()
{

}

void OptixDestroyableObject::set_destroyable_object(optix::DestroyableObj* object)
{
    this->object = object;
}

void OptixDestroyableObject::destroy()
{
    object->destroy();
}
void OptixDestroyableObject::validate()
{
    object->validate();
}


void OptixDestroyableObject::export_for_python()
{
    boost::python::class_<OptixDestroyableObject >(
                "_OptixDestroyableObject",
                "_OptixDestroyableObject docstring",
                boost::python::no_init)

            .def("destroy", &OptixDestroyableObject::destroy)
            .def("validate", &OptixDestroyableObject::validate);
}


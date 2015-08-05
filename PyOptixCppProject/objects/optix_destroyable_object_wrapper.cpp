#include "optix_destroyable_object_wrapper.h"




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



#include "Python.h"
#include <boost/python.hpp>
void OptixDestroyableObject::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixDestroyableObject >("_OptixDestroyableObject", "_OptixDestroyableObject docstring", bp::no_init)
            //*****************
            // DIRECT ACCESS
            //*****************
            .def("destroy", &OptixDestroyableObject::destroy)
            .def("validate", &OptixDestroyableObject::validate);
}


#include "optix_scoped_object_wrapper.h"
#include "Python.h"
#include <boost/python.hpp>


OptixScopedObjectWrapper::OptixScopedObjectWrapper()
{

}

void OptixScopedObjectWrapper::set_scoped_object(optix::ScopedObj* scoped_object)
{
    this->scoped_object = scoped_object;
    this->set_destroyable_object(scoped_object);
}

optix::Variable OptixScopedObjectWrapper::declare_variable(const std::string name)
{
    return this->scoped_object->declareVariable(name);
}

optix::Variable OptixScopedObjectWrapper::query_variable(const std::string name)
{
    return this->scoped_object->queryVariable(name);
}

optix::Variable OptixScopedObjectWrapper::get_variable(int index)
{
    return this->scoped_object->getVariable(index);
}

void OptixScopedObjectWrapper::remove_variable(optix::Variable variable)
{
    this->scoped_object->removeVariable(variable);
}

unsigned int OptixScopedObjectWrapper::get_variable_count()
{
    return this->scoped_object->getVariableCount();
}

void OptixScopedObjectWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixScopedObjectWrapper, bp::bases<OptixDestroyableObject> >(
                "_OptixScopedObjectWrapper",
                "_OptixScopedObjectWrapper docstring",
                bp::no_init)

            .def("_declare_variable", &OptixScopedObjectWrapper::declare_variable)
            .def("_query_variable", &OptixScopedObjectWrapper::query_variable)
            .def("_get_variable", &OptixScopedObjectWrapper::get_variable)
            .def("_remove_variable", &OptixScopedObjectWrapper::remove_variable)
            .def("get_variable_count", &OptixScopedObjectWrapper::get_variable_count);
}

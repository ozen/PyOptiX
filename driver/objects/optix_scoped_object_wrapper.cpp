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

OptixVariableWrapper* OptixScopedObjectWrapper::query_variable(const std::string name)
{
    optix::Variable variable = this->scoped_object->queryVariable(name);
    return new OptixVariableWrapper(variable);
}

OptixVariableWrapper* OptixScopedObjectWrapper::declare_variable(const std::string name)
{
    optix::Variable variable = this->scoped_object->declareVariable(name);
    return new OptixVariableWrapper(variable);
}

OptixVariableWrapper* OptixScopedObjectWrapper::get_variable(int index)
{
    optix::Variable variable = this->scoped_object->getVariable(index);
    return new OptixVariableWrapper(variable);
}

void OptixScopedObjectWrapper::remove_variable(OptixVariableWrapper* optix_variable_wrapper)
{
    this->scoped_object->removeVariable(optix_variable_wrapper->get_native());
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

            .def("_declare_variable", &OptixScopedObjectWrapper::declare_variable, bp::return_value_policy<bp::manage_new_object>())
            .def("_query_variable", &OptixScopedObjectWrapper::query_variable, bp::return_value_policy<bp::manage_new_object>())
            .def("_get_variable", &OptixScopedObjectWrapper::get_variable, bp::return_value_policy<bp::manage_new_object>())
            .def("_remove_variable", &OptixScopedObjectWrapper::remove_variable)
            .def("get_variable_count", &OptixScopedObjectWrapper::get_variable_count);
}

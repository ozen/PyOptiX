#include "scoped.h"


NativeScopedWrapper::NativeScopedWrapper() {}

void NativeScopedWrapper::set_scoped_object(optix::ScopedObj* scoped_object) {
    this->scoped_object = scoped_object;
    this->set_destroyable_object(scoped_object);
}

NativeVariableWrapper* NativeScopedWrapper::query_variable(const std::string name) {
    optix::Variable variable = this->scoped_object->queryVariable(name);
    return new NativeVariableWrapper(variable);
}

NativeVariableWrapper* NativeScopedWrapper::declare_variable(const std::string name) {
    optix::Variable variable = this->scoped_object->declareVariable(name);
    return new NativeVariableWrapper(variable);
}

NativeVariableWrapper* NativeScopedWrapper::get_variable(int index) {
    optix::Variable variable = this->scoped_object->getVariable(index);
    return new NativeVariableWrapper(variable);
}

void NativeScopedWrapper::remove_variable(NativeVariableWrapper* variable_wrapper) {
    this->scoped_object->removeVariable(variable_wrapper->get_native());
}

unsigned int NativeScopedWrapper::get_variable_count() {
    return this->scoped_object->getVariableCount();
}

void NativeScopedWrapper::export_for_python() {
    namespace bp = boost::python;

    bp::class_<NativeScopedWrapper, bp::bases<NativeDestroyableWrapper> >(
                "NativeScopedWrapper",
                "NativeScopedWrapper docstring",
                bp::no_init)

            .def("_declare_variable", &NativeScopedWrapper::declare_variable, bp::return_value_policy<bp::manage_new_object>())
            .def("_query_variable", &NativeScopedWrapper::query_variable, bp::return_value_policy<bp::manage_new_object>())
            .def("_get_variable", &NativeScopedWrapper::get_variable, bp::return_value_policy<bp::manage_new_object>())
            .def("_remove_variable", &NativeScopedWrapper::remove_variable)
            .def("get_variable_count", &NativeScopedWrapper::get_variable_count);
}

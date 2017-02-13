#include "scoped.h"


void NativeScopedWrapper::set_scoped_object(optix::ScopedObj* scoped_object) {
    this->scoped_object = scoped_object;
    this->set_destroyable_object(scoped_object);
}

NativeVariableWrapper* NativeScopedWrapper::query_variable(const std::string& name) {
    optix::Variable variable = this->scoped_object->queryVariable(name);
    if (variable == 0)
        return nullptr;
    else
        return new NativeVariableWrapper(variable);
}

NativeVariableWrapper* NativeScopedWrapper::declare_variable(const std::string& name) {
    return new NativeVariableWrapper(this->scoped_object->declareVariable(name));
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

void NativeScopedWrapper::boost_python_expose() {
    namespace bp = boost::python;

    bp::class_<NativeScopedWrapper, bp::bases<NativeDestroyableWrapper> >(
                "NativeScopedWrapper",
                "Wraps optix::Scoped class",
                bp::no_init)

            .def("declare_variable", &NativeScopedWrapper::declare_variable, bp::return_value_policy<bp::manage_new_object>())
            .def("query_variable", &NativeScopedWrapper::query_variable, bp::return_value_policy<bp::manage_new_object>())
            .def("get_variable", &NativeScopedWrapper::get_variable, bp::return_value_policy<bp::manage_new_object>())
            .def("remove_variable", &NativeScopedWrapper::remove_variable)
            .def("get_variable_count", &NativeScopedWrapper::get_variable_count);
}

#include "optix_program_wrapper.h"
#include "Python.h"
#include <boost/python.hpp>


OptixProgramWrapper::OptixProgramWrapper(optix::Program program)
{
    this->program = program;
    this->set_scoped_object(this->program.get());
}

OptixProgramWrapper::~OptixProgramWrapper()
{
    if(this->program.get() != 0)
        this->program->destroy();
}

int OptixProgramWrapper::get_id()
{
    return this->program->getId();
}

optix::Program OptixProgramWrapper::get_native_program()
{
    return this->program;
}

void OptixProgramWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::class_<OptixProgramWrapper, bp::bases<OptixScopedObjectWrapper> >(
                "_OptixProgramWrapper",
                "_OptixProgramWrapper docstring",
                bp::init<optix::Program>())

            .def("get_id", &OptixProgramWrapper::get_id);
}


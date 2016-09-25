#pragma once
#include "shared_includes.h"
#include "scoped.h"


class NativeProgramWrapper : public NativeScopedWrapper
{
private:
    optix::Program program;

public:
    NativeProgramWrapper(optix::Program program);
    ~NativeProgramWrapper();
    optix::Variable get_assignable_variable(const std::string& variable_name);
    int get_id();
    optix::Program get_native();
    static void export_for_python();
};

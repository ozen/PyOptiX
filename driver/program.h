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
    int get_id();
    optix::Program get_native();
    static void boost_python_expose();
};

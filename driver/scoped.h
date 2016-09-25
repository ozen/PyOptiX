#pragma once
#include "shared_includes.h"
#include "variable.h"
#include "destroyable.h"

class NativeScopedWrapper : public NativeDestroyableWrapper
{
private:
    optix::ScopedObj* scoped_object;

protected:
    void set_scoped_object(optix::ScopedObj* scoped_object);

public:
    NativeVariableWrapper* query_variable(const std::string name);
    NativeVariableWrapper* declare_variable(const std::string name);
    NativeVariableWrapper* get_variable(int index);
    void remove_variable(NativeVariableWrapper* variable_wrapper);
    unsigned int get_variable_count();
    static void export_for_python();
};

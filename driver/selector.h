#pragma once
#include "shared_includes.h"
#include "geometry_group.h"
#include "group.h"
#include "program.h"
#include "transform.h"
#include "scoped.h"
#include "destroyable.h"


class NativeSelectorWrapper : public NativeDestroyableWrapper
{
private:
    optix::Selector selector;

public:
    NativeSelectorWrapper(optix::Selector selector);
    void set_visit_program(NativeProgramWrapper* program);
    void set_child_count(unsigned int count);
    unsigned int get_child_count();
    void set_child_geometry_group(unsigned int index, NativeGeometryGroupWrapper* child);
    void set_child_group(unsigned int index, NativeGroupWrapper* child);
    void set_child_selector(unsigned int index, NativeSelectorWrapper* child);
    void set_child_transform(unsigned int index, NativeTransformWrapper* child);
    void remove_child(unsigned int index);
    optix::Selector get_native();
    static void export_for_python();
};

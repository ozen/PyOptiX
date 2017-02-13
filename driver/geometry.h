#pragma once
#include "shared_includes.h"
#include "program.h"
#include "scoped.h"


class NativeGeometryWrapper : public NativeScopedWrapper
{
private:
    optix::Geometry geometry;

public:
    NativeGeometryWrapper(optix::Geometry geometry);
    ~NativeGeometryWrapper();
    void mark_dirty();
    bool is_dirty();
    void set_primitive_count(unsigned int num_primitives);
    unsigned int get_primitive_count();
    void set_primitive_index_offset(unsigned int index_offset);
    unsigned int get_primitive_index_offset();
    void set_bounding_box_program(NativeProgramWrapper* program);
    void set_intersection_program(NativeProgramWrapper* program);
    optix::Geometry get_native();
    static void boost_python_expose();
};

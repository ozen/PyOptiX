#ifndef OPTIX_GEOMETRY_WRAPPER_H
#define OPTIX_GEOMETRY_WRAPPER_H

#include "shared_includes.h"
#include "optix_program_wrapper.h"
#include "optix_scoped_object_wrapper.h"


class OptixGeometryWrapper : public OptixScopedObjectWrapper
{
private:
    optix::Geometry geometry;

public:
    OptixGeometryWrapper(optix::Geometry geometry);
    ~OptixGeometryWrapper();

    void mark_dirty();
    bool is_dirty();
    void set_primitive_count(unsigned int  num_primitives);
    unsigned int get_primitive_count();
    void set_primitive_index_oOffset(unsigned int  index_offset);
    unsigned int get_primitive_index_offset();

    void set_bounding_box_program(OptixProgramWrapper*  program);
    void set_intersection_program(OptixProgramWrapper*  program);

    optix::Geometry get_native();

    static void export_for_python();
};


#endif

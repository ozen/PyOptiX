#ifndef OPTIX_TRANSFORM_WRAPPER_H
#define OPTIX_TRANSFORM_WRAPPER_H

#include "shared_includes.h"
#include "optix_program_wrapper.h"
#include "optix_destroyable_object_wrapper.h"


class OptixSelectorWrapper;
class OptixGroupWrapper;
class OptixGeometryGroupWrapper;

class OptixTransformWrapper: public OptixDestroyableObject
{
private:
    optix::Transform transform;
public:
    OptixTransformWrapper(optix::Transform transform);
    ~OptixTransformWrapper();

    void set_matrix();
    void get_matrix();

    void set_child_geometry_group(unsigned int index, OptixGeometryGroupWrapper* child);
    void set_child_group(unsigned int index, OptixGroupWrapper* child);
    void set_child_selector(unsigned int index, OptixSelectorWrapper* child);
    void set_child_transform(unsigned int index, OptixGeometryGroupWrapper* child);

    optix::Transform get_native();

    static void export_for_python();
};

#endif

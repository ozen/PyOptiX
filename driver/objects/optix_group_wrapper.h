#ifndef OPTIX_GROUP_WRAPPER_H
#define OPTIX_GROUP_WRAPPER_H

#include "shared_includes.h"
#include "optix_acceleration_wrapper.h"
#include "optix_geometry_instance_wrapper.h"
#include "optix_transform_wrapper.h"
#include "optix_scoped_object_wrapper.h"
#include "optix_destroyable_object_wrapper.h"

class OptixGeometryGroupWrapper;
class OptixSelectorWrapper;

class OptixGroupWrapper: public OptixDestroyableObject
{
private:
    optix::Group group;

public:
    OptixGroupWrapper(optix::Group group);
    ~OptixGroupWrapper();

    void set_acceleration(OptixAccelerationWrapper* acceleration);
    void set_child_count(unsigned int count);
    unsigned int get_child_count();

    void set_child_geometry_group(unsigned int index, OptixGeometryGroupWrapper* child);
    void set_child_group(unsigned int index, OptixGroupWrapper* child);
    void set_child_selector(unsigned int index, OptixSelectorWrapper* child);
    void set_child_transform(unsigned int index, OptixTransformWrapper* child);
    void set_child_acceleration(unsigned int index, OptixAccelerationWrapper* child);

    void remove_child(unsigned int index);

    optix::Group get_native();

    static void export_for_python();
};

#include "optix_geometry_group_wrapper.h"
#include "optix_selector_wrapper.h"


#endif

#ifndef OPTIX_GEOMETRY_GROUP_WRAPPER_H
#define OPTIX_GEOMETRY_GROUP_WRAPPER_H

#include "shared_includes.h"

#include "optix_acceleration_wrapper.h"
#include "optix_geometry_instance_wrapper.h"

#include "optix_scoped_object_wrapper.h"

#include "optix_destroyable_object_wrapper.h"

class OptixGeometryGroupWrapper: public OptixDestroyableObject
{
private:
    optix::GeometryGroup geometry_group;
public:
    OptixGeometryGroupWrapper(optix::GeometryGroup geometry_group);
    ~OptixGeometryGroupWrapper();

    void set_acceleration(OptixAccelerationWrapper* acceleration);

    void set_child_count(unsigned int  count);
    unsigned int get_child_count();

    void set_child_geometry_group_instance(unsigned int index, OptixGeometryInstanceWrapper* geometryinstance);

    void remove_child(unsigned int index);

    optix::GeometryGroup get_native();

    static void export_for_python();

};


#endif

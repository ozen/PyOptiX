#ifndef OPTIX_GEOMETRY_INSTANCE_WRAPPER_H
#define OPTIX_GEOMETRY_INSTANCE_WRAPPER_H



#include "optix_shared_includes.h"

#include "optix_geometry_wrapper.h"
#include "optix_material_wrapper.h"

#include "optix_scoped_object_wrapper.h"

class OptixGeometryInstanceWrapper : public OptixScopedObjectWrapper
{
private:
    optix::GeometryInstance geometry_instance;
public:
    OptixGeometryInstanceWrapper(optix::GeometryInstance geometry_instance);
    ~OptixGeometryInstanceWrapper();

    void set_geometry(OptixGeometryWrapper* geometry);

    void set_material_count(unsigned int count);
    unsigned int get_material_count();

    void set_material(unsigned int idx, OptixMaterialWrapper* material);

    optix::GeometryInstance get_native();

    static void export_for_python();

};











#endif

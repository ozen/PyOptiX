#pragma once
#include "shared_includes.h"
#include "geometry.h"
#include "material.h"
#include "scoped.h"


class NativeGeometryInstanceWrapper : public NativeScopedWrapper
{
private:
    optix::GeometryInstance geometry_instance;

public:
    NativeGeometryInstanceWrapper(optix::GeometryInstance geometry_instance);
    ~NativeGeometryInstanceWrapper();
    void set_geometry(NativeGeometryWrapper* geometry);
    void set_material_count(unsigned int count);
    unsigned int get_material_count();
    void set_material(unsigned int idx, NativeMaterialWrapper* material);
    optix::GeometryInstance get_native();
    static void boost_python_expose();
};

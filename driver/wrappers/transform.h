#pragma once
#include "shared_includes.h"
#include "program.h"
#include "destroyable.h"

class NativeSelectorWrapper;
class NativeGroupWrapper;
class NativeGeometryGroupWrapper;

class NativeTransformWrapper : public NativeDestroyableWrapper
{
private:
    optix::Transform transform;

public:
    NativeTransformWrapper(optix::Transform transform);
    ~NativeTransformWrapper();
    void set_matrix(bool transpose, const boost::numpy::ndarray& array);
    boost::numpy::ndarray get_matrix(bool transpose);
    void set_child_geometry_group(unsigned int index, NativeGeometryGroupWrapper* child);
    void set_child_group(unsigned int index, NativeGroupWrapper* child);
    void set_child_selector(unsigned int index, NativeSelectorWrapper* child);
    void set_child_transform(unsigned int index, NativeGeometryGroupWrapper* child);
    optix::Transform get_native();
    static void export_for_python();
};

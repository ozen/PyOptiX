#pragma once
#include "shared_includes.h"

class NativeBufferWrapper;
class NativeTextureSamplerWrapper;
class NativeProgramWrapper;
class NativeGroupWrapper;
class NativeGeometryGroupWrapper;
class NativeTransformWrapper;
class NativeSelectorWrapper;


class NativeVariableWrapper
{
private:
    optix::Variable variable;

public:
    NativeVariableWrapper(optix::Variable variable);
    ~NativeVariableWrapper();
    bool is_valid();
    std::string get_name();
    std::string get_annotation();
    RTobjecttype get_type();
    unsigned long get_size_in_bytes();
    void set_buffer(NativeBufferWrapper* buffer_wrapper);
    void set_texture(NativeTextureSamplerWrapper* texture_wrapper);
    void set_program_id_with_program(NativeProgramWrapper* program_wrapper);
    void set_group(NativeGroupWrapper* group_wrapper);
    void set_geometry_group(NativeGeometryGroupWrapper* geometry_group_wrapper);
    void set_transform(NativeTransformWrapper* transform_wrapper);
    void set_selector(NativeSelectorWrapper* selector_wrapper);
    void set_from_numpy(const boost::numpy::ndarray& numpy_array);
    void set_from_numpy_with_type(const boost::numpy::ndarray& numpy_array, RTobjecttype object_type);
    optix::Variable get_native();
    static void export_for_python();
};

#ifndef OPTIX_VARIABLE_WRAPPER_H
#define OPTIX_VARIABLE_WRAPPER_H

#include "optix_shared_includes.h"
#include "boost/python.hpp"
#include "boost/numpy.hpp"


class OptixBufferWrapper;
class OptixTextureSamplerWrapper;
class OptixProgramWrapper;
class OptixGroupWrapper;
class OptixGeometryGroupWrapper;
class OptixTransformWrapper;
class OptixSelectorWrapper;


class OptixVariableWrapper
{
private:
    optix::Variable variable;

public:
    OptixVariableWrapper(optix::Variable variable);

    bool is_valid();

    std::string get_name();
    std::string get_annotation();

    RTobjecttype get_type();

    unsigned long get_size_in_bytes();

    optix::Variable get_variable_native();

    void set_buffer(OptixBufferWrapper* buffer_wrapper);
    void set_texture(OptixTextureSamplerWrapper* texture_wrapper);
    void set_program_id_with_program(OptixProgramWrapper* program_wrapper);
    void set_group(OptixGroupWrapper* group_wrapper);
    void set_geometry_group(OptixGeometryGroupWrapper* geometry_group_wrapper);
    void set_transform(OptixTransformWrapper* transform_wrapper);
    void set_selector(OptixSelectorWrapper* selector_wrapper);

    void set_with_numpy_array1x1_dtype(const boost::numpy::ndarray& numpy_array1x1);
    void set_variable_with_type(const boost::numpy::ndarray& numpy_array, RTobjecttype object_type);

    static void export_for_python();

};


#endif

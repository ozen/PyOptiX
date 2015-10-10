#ifndef OPTIX_VARIABLE_WRAPPER_H
#define OPTIX_VARIABLE_WRAPPER_H

#include "shared_includes.h"
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

    void set_buffer(OptixBufferWrapper* buffer_wrapper);
    void set_texture(OptixTextureSamplerWrapper* texture_wrapper);
    void set_program_id_with_program(OptixProgramWrapper* program_wrapper);
    void set_group(OptixGroupWrapper* group_wrapper);
    void set_geometry_group(OptixGeometryGroupWrapper* geometry_group_wrapper);
    void set_transform(OptixTransformWrapper* transform_wrapper);
    void set_selector(OptixSelectorWrapper* selector_wrapper);

    void set_from_numpy(const boost::numpy::ndarray& numpy_array);
    void set_from_numpy_with_type(const boost::numpy::ndarray& numpy_array, RTobjecttype object_type);

    optix::Variable get_native();

    static void export_for_python();
};


#endif

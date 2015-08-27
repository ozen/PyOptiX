#ifndef OPTIX_ACCELERATION_WRAPPER_H
#define OPTIX_ACCELERATION_WRAPPER_H

#include "shared_includes.h"
#include "optix_destroyable_object_wrapper.h"

class OptixAccelerationWrapper: public OptixDestroyableObject
{
private:
    optix::Acceleration acceleration;

public:
    OptixAccelerationWrapper(optix::Acceleration acceleration);
    ~OptixAccelerationWrapper();

    void set_property(std::string name, std::string value_name);

    void mark_dirty();
    bool is_dirty();

    optix::Acceleration get_native();

    static void export_for_python();
};



#endif

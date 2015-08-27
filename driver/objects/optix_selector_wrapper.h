#ifndef OPTIX_SELECTOR_WRAPPER_H
#define OPTIX_SELECTOR_WRAPPER_H

#include "shared_includes.h"

#include "optix_geometry_group_wrapper.h"
#include "optix_group_wrapper.h"
#include "optix_program_wrapper.h"
#include "optix_transform_wrapper.h"

#include "optix_scoped_object_wrapper.h"

#include "optix_destroyable_object_wrapper.h"

class OptixSelectorWrapper: public OptixDestroyableObject
{
private:
    optix::Selector selector;
public:
    OptixSelectorWrapper(optix::Selector selector);
    ~OptixSelectorWrapper();

    void set_visit_program(OptixProgramWrapper*  program);

    void set_child_count(unsigned int count);
    unsigned int get_child_count();

    void set_child_geometry_group(unsigned int index, OptixGeometryGroupWrapper* child);
    void set_child_group(unsigned int index, OptixGroupWrapper* child);
    void set_child_selector(unsigned int index, OptixSelectorWrapper* child);
    void set_child_transform(unsigned int index, OptixTransformWrapper* child);

    void remove_child(unsigned int index);


    optix::Selector get_native();

    static void export_for_python();
};


#endif

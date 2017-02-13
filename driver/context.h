#pragma once
#include "shared_includes.h"
#include "buffer.h"
#include "program.h"
#include "texture_sampler.h"
#include "geometry.h"
#include "material.h"
#include "geometry_instance.h"
#include "group.h"
#include "geometry_group.h"
#include "transform.h"
#include "selector.h"
#include "acceleration.h"
#include "scoped.h"


class NativeContextWrapper : public NativeScopedWrapper
{
private:
    optix::Context context;

public:
    NativeContextWrapper();
    ~NativeContextWrapper();
    unsigned int get_ray_type_count();
    unsigned int get_entry_point_count();
    void set_ray_type_count(unsigned int ray_type_count);
    void set_entry_point_count(unsigned int entry_point_count);
    void set_ray_generation_program(unsigned int entry_point_index, NativeProgramWrapper* ray_generation_program);
    void set_exception_program(unsigned int entry_point_index, NativeProgramWrapper* exception_program);
    void set_miss_program(unsigned int ray_type_index, NativeProgramWrapper* miss_program);
    void compile();
    void launch_1d(unsigned int entry_point_index, int width);
    void launch_2d(unsigned int entry_point_index, int width, int height);
    void launch_3d(unsigned int entry_point_index, int width, int height, int depth);
    int get_cpu_num_of_threads();
    void set_cpu_num_of_threads(int threadCount);
    int get_stack_size();
    void set_stack_size(int stack_size_bytes);
    int get_available_devices_count();
    std::string get_device_name(int device_id);
    boost::python::tuple get_device_compute_capability(int device_id);
    int get_enabled_device_count();
    std::vector<int> get_enabled_devices();
    void set_devices(std::vector<int> devices);
    unsigned long get_used_host_memory();
    unsigned long get_available_device_memory(int device_id);
    void set_exception_enabled(RTexception exception, bool enabled);
    bool get_exception_enabled(RTexception exception);
    void set_print_enabled(bool enabled);
    bool get_print_enabled();
    void set_print_buffer_size(int buffer_size_bytes);
    int get_print_buffer_size();
    NativeProgramWrapper* create_program_from_file(std::string file_name, std::string function_name);
    NativeBufferWrapper* create_buffer(int buffer_type);
    NativeTextureSamplerWrapper* create_texture_sampler();
    NativeGeometryWrapper* create_geometry();
    NativeMaterialWrapper* create_material();
    NativeGeometryInstanceWrapper* create_geometry_instance();
    NativeGroupWrapper* create_group();
    NativeGeometryGroupWrapper* create_geometry_group();
    NativeTransformWrapper* create_transform();
    NativeSelectorWrapper* create_selector();
    NativeAccelerationWrapper* create_accelerator(std::string builder, std::string traverser);
    static void boost_python_expose();
};

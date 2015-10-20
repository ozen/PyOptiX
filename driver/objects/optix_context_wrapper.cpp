#include "optix_context_wrapper.h"
#include <iostream>
#include "Python.h"


OptixContextWrapper::OptixContextWrapper(): OptixScopedObjectWrapper()
{
    this->context = optix::Context::create();
    this->set_scoped_object(this->context.get());
}

OptixContextWrapper::~OptixContextWrapper()
{
    if(this->context.get() != 0)
        this->context->destroy();
}

optix::Variable OptixContextWrapper::get_assignable_variable(const std::string& variable_name)
{
    return this->context[variable_name];
}

unsigned int OptixContextWrapper::get_ray_type_count()
{
    return this->context->getRayTypeCount();
}

unsigned int OptixContextWrapper::get_entry_point_count()
{
    return this->context->getEntryPointCount();
}

void OptixContextWrapper::set_ray_type_count(unsigned int ray_type_count)
{
    this->context->setRayTypeCount(ray_type_count);
}

void OptixContextWrapper::set_entry_point_count(unsigned int entry_point_count)
{
    this->context->setEntryPointCount(entry_point_count);
}

void OptixContextWrapper::set_ray_generation_program(unsigned int entry_point_index, OptixProgramWrapper* ray_generation_program)
{
    this->context->setRayGenerationProgram(entry_point_index, ray_generation_program->get_native_program());
}

void OptixContextWrapper::set_exception_program(unsigned int entry_point_index, OptixProgramWrapper* exception_program)
{
    this->context->setExceptionProgram(entry_point_index, exception_program->get_native_program());
}

void OptixContextWrapper::set_miss_program(unsigned int ray_type_index, OptixProgramWrapper* miss_program)
{
    this->context->setMissProgram(ray_type_index, miss_program->get_native_program());
}

void OptixContextWrapper::compile()
{
    this->context->compile();
}

void OptixContextWrapper::launch_1d(unsigned int entry_point_index, int width)
{
    this->context->launch(entry_point_index, width);
}

void OptixContextWrapper::launch_2d(unsigned int entry_point_index, int width, int height)
{
    this->context->launch(entry_point_index, width, height);
}

void OptixContextWrapper::launch_3d(unsigned int entry_point_index, int width, int height, int depth)
{
    this->context->launch(entry_point_index, width, height, depth);
}

// CPU
int OptixContextWrapper::get_cpu_num_of_threads()
{
    return context->getCPUNumThreads();
}

void OptixContextWrapper::set_cpu_num_of_threads( int threadCount)
{
    context->setCPUNumThreads( threadCount);
}

// Multi GPU Device
int OptixContextWrapper::get_available_devices_count()
{
    return optix::Context::getDeviceCount();
}

std::string OptixContextWrapper::get_device_name( int deviceId)
{
    return context->getDeviceName( deviceId);
}

int OptixContextWrapper::get_enabled_device_count()
{
    return context->getEnabledDeviceCount();
}

std::vector<int> OptixContextWrapper::get_enabled_devices()
{
    return context->getEnabledDevices();
}

void OptixContextWrapper::set_devices(std::vector<int> devices)
{
    context->setDevices(devices.begin(), devices.end());
}

// Memory
unsigned long OptixContextWrapper::get_used_host_memory()
{
    return static_cast<unsigned long>(context->getUsedHostMemory());
}
unsigned long OptixContextWrapper::get_available_device_memory(int deviceId)
{
    return static_cast<unsigned long>( context->getAvailableDeviceMemory(deviceId));
}

// Exceptions
void OptixContextWrapper::set_exception_enabled(RTexception exception, bool enabled)
{
    this->context->setExceptionEnabled(exception, enabled);
}

bool OptixContextWrapper::get_exception_enabled(RTexception exception)
{
    return this->context->getExceptionEnabled(exception);
}

// Print
void OptixContextWrapper::set_print_enabled(bool enabled)
{
    this->context->setPrintEnabled(enabled);
}

bool OptixContextWrapper::get_print_enabled()
{
    return this->context->getPrintEnabled();
}


// *********************************
// OBJECTS
// *********************************

optix::Program OptixContextWrapper::create_program_from_file(std::string file_name, std::string program_name)
{
    return this->context->createProgramFromPTXFile(file_name, program_name);
}

optix::Buffer OptixContextWrapper::create_buffer(int buffer_type)
{
    return this->context->createBuffer(buffer_type);
}


optix::TextureSampler OptixContextWrapper::create_texture_sampler()
{
    return this->context->createTextureSampler();
}

optix::Geometry OptixContextWrapper::create_geometry()
{
    return this->context->createGeometry();
}

optix::Material OptixContextWrapper::create_material()
{
    return this->context->createMaterial();
}

optix::GeometryInstance OptixContextWrapper::create_geometry_instance()
{
    return this->context->createGeometryInstance();
}

optix::Group OptixContextWrapper::create_group()
{
    return this->context->createGroup();
}

optix::GeometryGroup OptixContextWrapper::create_geometry_group()
{
    return this->context->createGeometryGroup();
}

optix::Transform OptixContextWrapper::create_transform()
{
    return this->context->createTransform();
}

optix::Selector OptixContextWrapper::create_selector()
{
    return this->context->createSelector();
}

optix::Acceleration OptixContextWrapper::create_accelerator(std::string builder, std::string traverser)
{
    return this->context->createAcceleration(builder.c_str(), traverser.c_str());
}


// *********************************
// *********************************
// PYTHON SUPPORT
// *********************************
// *********************************


template<class T>
struct VecToList
{
    static PyObject* convert(const std::vector<T>& vec)
    {
        boost::python::list* l = new boost::python::list();
        for(size_t i = 0; i < vec.size(); i++)
            (*l).append(vec[i]);

        return l->ptr();
    }
};

void OptixContextWrapper::export_for_python()
{
    namespace bp = boost::python;

    bp::to_python_converter<std::vector<int,class std::allocator<int> >, VecToList<int> >();

    bp::class_<OptixContextWrapper, bp::bases<OptixScopedObjectWrapper> >(
                "_OptixContextWrapper",
                "_OptixContextWrapper docstring",
                bp::init<>())

            //*****************
            // DIRECT ACCESS
            //*****************

            .def("get_ray_type_count", &OptixContextWrapper::get_ray_type_count)
            .def("set_ray_type_count", &OptixContextWrapper::set_ray_type_count)

            .def("get_entry_point_count", &OptixContextWrapper::get_entry_point_count)
            .def("set_entry_point_count", &OptixContextWrapper::set_entry_point_count)

            // CPU
            .def("get_cpu_num_of_threads", &OptixContextWrapper::get_cpu_num_of_threads)
            .def("set_cpu_num_of_threads", &OptixContextWrapper::set_cpu_num_of_threads)

            // Multi GPU Device
            .def("get_available_devices_count", &OptixContextWrapper::get_available_devices_count)
            .def("get_device_name", &OptixContextWrapper::get_device_name)
            .def("get_enabled_device_count", &OptixContextWrapper::get_enabled_device_count)
            .def("get_enabled_devices", &OptixContextWrapper::get_enabled_devices)
            .def("set_devices", &OptixContextWrapper::set_devices)

            // Memory
            .def("get_used_host_memory", &OptixContextWrapper::get_used_host_memory)
            .def("get_available_device_memory", &OptixContextWrapper::get_available_device_memory)

            // Exceptions
            .def("get_exception_enabled", &OptixContextWrapper::get_exception_enabled)
            .def("set_exception_enabled", &OptixContextWrapper::set_exception_enabled)

            // Print
            .def("get_print_enabled", &OptixContextWrapper::get_print_enabled)
            .def("set_print_enabled", &OptixContextWrapper::set_print_enabled)

            // Programs
            .def("set_ray_generation_program", &OptixContextWrapper::set_ray_generation_program)
            .def("set_exception_program", &OptixContextWrapper::set_exception_program)
            .def("compile", &OptixContextWrapper::compile)

            //*****************
            // CONTROLLED ACCESS
            //*****************

            .def("_create_program_from_file", &OptixContextWrapper::create_program_from_file)
            .def("_create_buffer", &OptixContextWrapper::create_buffer)
            .def("_create_texture_sampler", &OptixContextWrapper::create_texture_sampler)
            .def("_create_geometry", &OptixContextWrapper::create_geometry)
            .def("_create_material", &OptixContextWrapper::create_material)
            .def("_create_geometry_instance", &OptixContextWrapper::create_geometry_instance)
            .def("_create_group", &OptixContextWrapper::create_group)
            .def("_create_geometry_group", &OptixContextWrapper::create_geometry_group)
            .def("_create_transform", &OptixContextWrapper::create_transform)
            .def("_create_selector", &OptixContextWrapper::create_selector)
            .def("_create_accelerator", &OptixContextWrapper::create_accelerator)

            .def("_set_miss_program", &OptixContextWrapper::set_miss_program)

            .def("_launch_1d", &OptixContextWrapper::launch_1d)
            .def("_launch_2d", &OptixContextWrapper::launch_2d)
            .def("_launch_3d", &OptixContextWrapper::launch_3d);

}

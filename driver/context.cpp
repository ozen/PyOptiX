#include "context.h"


NativeContextWrapper::NativeContextWrapper(): NativeScopedWrapper() {
    this->context = optix::Context::create();
    this->set_scoped_object(this->context.get());
}

NativeContextWrapper::~NativeContextWrapper() {
    this->context->destroy();
}

unsigned int NativeContextWrapper::get_ray_type_count() {
    return this->context->getRayTypeCount();
}

unsigned int NativeContextWrapper::get_entry_point_count() {
    return this->context->getEntryPointCount();
}

void NativeContextWrapper::set_ray_type_count(unsigned int ray_type_count) {
    this->context->setRayTypeCount(ray_type_count);
}

void NativeContextWrapper::set_entry_point_count(unsigned int entry_point_count) {
    this->context->setEntryPointCount(entry_point_count);
}

void NativeContextWrapper::set_ray_generation_program(unsigned int entry_point_index, NativeProgramWrapper* ray_generation_program) {
    this->context->setRayGenerationProgram(entry_point_index, ray_generation_program->get_native());
}

void NativeContextWrapper::set_exception_program(unsigned int entry_point_index, NativeProgramWrapper* exception_program) {
    this->context->setExceptionProgram(entry_point_index, exception_program->get_native());
}

void NativeContextWrapper::set_miss_program(unsigned int ray_type_index, NativeProgramWrapper* miss_program) {
    this->context->setMissProgram(ray_type_index, miss_program->get_native());
}

void NativeContextWrapper::compile() {
    this->context->compile();
}

void NativeContextWrapper::launch_1d(unsigned int entry_point_index, int width) {
    this->context->launch(entry_point_index, width);
}

void NativeContextWrapper::launch_2d(unsigned int entry_point_index, int width, int height) {
    this->context->launch(entry_point_index, width, height);
}

void NativeContextWrapper::launch_3d(unsigned int entry_point_index, int width, int height, int depth) {
    this->context->launch(entry_point_index, width, height, depth);
}

int NativeContextWrapper::get_cpu_num_of_threads() {
    return context->getCPUNumThreads();
}

void NativeContextWrapper::set_cpu_num_of_threads(int threadCount) {
    context->setCPUNumThreads(threadCount);
}

int NativeContextWrapper::get_stack_size() {
    return context->getStackSize();
}

void NativeContextWrapper::set_stack_size(int stack_size_bytes) {
    context->setStackSize(stack_size_bytes);
}


int NativeContextWrapper::get_available_devices_count() {
    return optix::Context::getDeviceCount();
}

std::string NativeContextWrapper::get_device_name(int device_id) {
    return context->getDeviceName(device_id);
}

boost::python::tuple NativeContextWrapper::get_device_compute_capability(int device_id) {
    int computeCapabilities[2];
    context->getDeviceAttribute(device_id, RT_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY, sizeof(computeCapabilities), computeCapabilities);
    return boost::python::make_tuple(computeCapabilities[0], computeCapabilities[1]);
}

int NativeContextWrapper::get_enabled_device_count() {
    return context->getEnabledDeviceCount();
}

std::vector<int> NativeContextWrapper::get_enabled_devices() {
    return context->getEnabledDevices();
}

void NativeContextWrapper::set_devices(std::vector<int> devices) {
    context->setDevices(devices.begin(), devices.end());
}

unsigned long NativeContextWrapper::get_used_host_memory() {
    return static_cast<unsigned long>(context->getUsedHostMemory());
}

unsigned long NativeContextWrapper::get_available_device_memory(int device_id) {
    return static_cast<unsigned long>(context->getAvailableDeviceMemory(device_id));
}

void NativeContextWrapper::set_exception_enabled(RTexception exception, bool enabled) {
    this->context->setExceptionEnabled(exception, enabled);
}

bool NativeContextWrapper::get_exception_enabled(RTexception exception) {
    return this->context->getExceptionEnabled(exception);
}

void NativeContextWrapper::set_print_enabled(bool enabled){
    this->context->setPrintEnabled(enabled);
}

bool NativeContextWrapper::get_print_enabled() {
    return this->context->getPrintEnabled();
}

void NativeContextWrapper::set_print_buffer_size(int buffer_size_bytes){
    this->context->setPrintBufferSize(buffer_size_bytes);
}

int NativeContextWrapper::get_print_buffer_size() {
    return this->context->getPrintBufferSize();
}

NativeProgramWrapper* NativeContextWrapper::create_program_from_file(std::string file_name, std::string program_name) {
    return new NativeProgramWrapper(this->context->createProgramFromPTXFile(file_name, program_name));
}

NativeBufferWrapper* NativeContextWrapper::create_buffer(int buffer_type) {
    return new NativeBufferWrapper(this->context->createBuffer(buffer_type));
}

NativeTextureSamplerWrapper* NativeContextWrapper::create_texture_sampler() {
    return new NativeTextureSamplerWrapper(this->context->createTextureSampler());
}

NativeGeometryWrapper* NativeContextWrapper::create_geometry() {
    return new NativeGeometryWrapper(this->context->createGeometry());
}

NativeMaterialWrapper* NativeContextWrapper::create_material() {
    return new NativeMaterialWrapper(this->context->createMaterial());
}

NativeGeometryInstanceWrapper* NativeContextWrapper::create_geometry_instance() {
    return new NativeGeometryInstanceWrapper(this->context->createGeometryInstance());
}

NativeGroupWrapper* NativeContextWrapper::create_group() {
    return new NativeGroupWrapper(this->context->createGroup());
}

NativeGeometryGroupWrapper* NativeContextWrapper::create_geometry_group() {
    return new NativeGeometryGroupWrapper(this->context->createGeometryGroup());
}

NativeTransformWrapper* NativeContextWrapper::create_transform() {
    return new NativeTransformWrapper(this->context->createTransform());
}

NativeSelectorWrapper* NativeContextWrapper::create_selector() {
    return new NativeSelectorWrapper(this->context->createSelector());
}

NativeAccelerationWrapper* NativeContextWrapper::create_accelerator(std::string builder, std::string traverser) {
    return new NativeAccelerationWrapper(this->context->createAcceleration(builder.c_str(), traverser.c_str()));
}

void NativeContextWrapper::boost_python_expose() {
    namespace bp = boost::python;

    bp::class_<NativeContextWrapper, bp::bases<NativeScopedWrapper> >(
                "NativeContextWrapper",
                "Wraps optix::Context class",
                bp::init<>())

            .def("get_ray_type_count", &NativeContextWrapper::get_ray_type_count)
            .def("set_ray_type_count", &NativeContextWrapper::set_ray_type_count)
            .def("get_entry_point_count", &NativeContextWrapper::get_entry_point_count)
            .def("set_entry_point_count", &NativeContextWrapper::set_entry_point_count)
            .def("get_cpu_num_of_threads", &NativeContextWrapper::get_cpu_num_of_threads)
            .def("set_cpu_num_of_threads", &NativeContextWrapper::set_cpu_num_of_threads)
            .def("get_stack_size", &NativeContextWrapper::get_stack_size)
            .def("set_stack_size", &NativeContextWrapper::set_stack_size)
            .def("get_available_devices_count", &NativeContextWrapper::get_available_devices_count)
            .def("get_device_name", &NativeContextWrapper::get_device_name)
            .def("get_device_compute_capability", &NativeContextWrapper::get_device_compute_capability)
            .def("get_enabled_device_count", &NativeContextWrapper::get_enabled_device_count)
            .def("get_enabled_devices", &NativeContextWrapper::get_enabled_devices)
            .def("set_devices", &NativeContextWrapper::set_devices)
            .def("get_used_host_memory", &NativeContextWrapper::get_used_host_memory)
            .def("get_available_device_memory", &NativeContextWrapper::get_available_device_memory)
            .def("get_exception_enabled", &NativeContextWrapper::get_exception_enabled)
            .def("set_exception_enabled", &NativeContextWrapper::set_exception_enabled)
            .def("get_print_enabled", &NativeContextWrapper::get_print_enabled)
            .def("set_print_enabled", &NativeContextWrapper::set_print_enabled)
            .def("get_print_buffer_size", &NativeContextWrapper::get_print_buffer_size)
            .def("set_print_buffer_size", &NativeContextWrapper::set_print_buffer_size)
            .def("set_ray_generation_program", &NativeContextWrapper::set_ray_generation_program)
            .def("set_exception_program", &NativeContextWrapper::set_exception_program)
            .def("set_miss_program", &NativeContextWrapper::set_miss_program)
            .def("compile", &NativeContextWrapper::compile)
            .def("create_program_from_file", &NativeContextWrapper::create_program_from_file, bp::return_value_policy<bp::manage_new_object>())
            .def("create_buffer", &NativeContextWrapper::create_buffer, bp::return_value_policy<bp::manage_new_object>())
            .def("create_texture_sampler", &NativeContextWrapper::create_texture_sampler, bp::return_value_policy<bp::manage_new_object>())
            .def("create_geometry", &NativeContextWrapper::create_geometry, bp::return_value_policy<bp::manage_new_object>())
            .def("create_material", &NativeContextWrapper::create_material, bp::return_value_policy<bp::manage_new_object>())
            .def("create_geometry_instance", &NativeContextWrapper::create_geometry_instance, bp::return_value_policy<bp::manage_new_object>())
            .def("create_group", &NativeContextWrapper::create_group, bp::return_value_policy<bp::manage_new_object>())
            .def("create_geometry_group", &NativeContextWrapper::create_geometry_group, bp::return_value_policy<bp::manage_new_object>())
            .def("create_transform", &NativeContextWrapper::create_transform, bp::return_value_policy<bp::manage_new_object>())
            .def("create_selector", &NativeContextWrapper::create_selector, bp::return_value_policy<bp::manage_new_object>())
            .def("create_accelerator", &NativeContextWrapper::create_accelerator, bp::return_value_policy<bp::manage_new_object>())
            .def("launch_1d", &NativeContextWrapper::launch_1d)
            .def("launch_2d", &NativeContextWrapper::launch_2d)
            .def("launch_3d", &NativeContextWrapper::launch_3d);
}
